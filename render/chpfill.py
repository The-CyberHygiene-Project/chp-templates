# CyberHygiene Project — chp-templates (shared SSP and POA&M templates).
# Licensed under the Apache License 2.0. Placeholder templates only: no site's values belong in this repository.
"""chpfill: fill chp-templates placeholders (spec 2026-10-24 §3). Python 3.9, standard library only.

Syntax: {{section.key}}, {{section.key | list}}, and line-level blocks {{#if facts.name}} ... {{/if}}.
Fill is single pass: an inserted value is never scanned again. Unfilled placeholders stay as written and are reported."""
import re

TOKEN = re.compile(r"\{\{([a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+)(?:\s*\|\s*([A-Za-z_]+))?\}\}")
IF_OPEN = re.compile(r"^\{\{#if (facts\.[a-z0-9_]+)\}\}$")
IF_CLOSE = "{{/if}}"
FILTERS = {"list"}


class FillError(Exception):
    """A template or input error; the message starts with '<source>:<line>: '."""


def _render_value(value, filt):
    if filt == "list":
        items = value if isinstance(value, list) else [value]
        return "\n".join(f"- {i}" for i in items)
    return ", ".join(value) if isinstance(value, list) else str(value)


def _sub_line(line, lineno, values, src, unfilled):
    def repl(m):
        key, filt = m.group(1), m.group(2)
        if filt is not None and filt not in FILTERS:
            raise FillError(f"{src}:{lineno}: unknown filter {filt}")
        if key not in values:
            unfilled.append((key, lineno))
            return m.group(0)
        return _render_value(values[key], filt)
    return TOKEN.sub(repl, line)


def fill_text(text, values, facts, src):
    """Return (filled text, [(unfilled key, line), ...]). Raises FillError on a malformed block or unknown filter."""
    out, unfilled = [], []
    block = None                     # (fact, open line number, open line text, [(lineno, line), ...])
    for lineno, line in enumerate(text.splitlines(keepends=True), 1):
        stripped = line.strip()
        m = IF_OPEN.match(stripped)
        if m:
            if block is not None:
                raise FillError(f"{src}:{lineno}: nested {{{{#if}}}} is not allowed")
            block = (m.group(1), lineno, line, [])
            continue
        if stripped == IF_CLOSE:
            if block is None:
                raise FillError(f"{src}:{lineno}: {{{{/if}}}} without an open {{{{#if}}}}")
            fact, open_no, open_line, body = block
            block = None
            if fact not in facts:
                unfilled.append((fact, open_no))
                out.append(open_line)
                out.extend(_sub_line(b, n, values, src, unfilled) for n, b in body)
                out.append(line)
            elif facts[fact]:
                out.extend(_sub_line(b, n, values, src, unfilled) for n, b in body)
            else:
                for n, b in body:            # still validate the skipped text: errors always stop the run
                    _sub_line(b, n, values, src, [])
                out.append(f"*Not applicable: {fact} = no.*" + ("\n" if line.endswith("\n") else ""))
            continue
        if block is not None:
            block[3].append((lineno, line))
        else:
            out.append(_sub_line(line, lineno, values, src, unfilled))
    if block is not None:
        raise FillError(f"{src}:{block[1]}: unclosed {{{{#if {block[0]}}}}}")
    return "".join(out), unfilled
