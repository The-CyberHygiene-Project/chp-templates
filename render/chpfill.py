# CyberHygiene Project — chp-templates (shared SSP and POA&M templates).
# Licensed under the Apache License 2.0. Placeholder templates only: no site's values belong in this repository.
"""chpfill: fill chp-templates placeholders (spec 2026-10-24 §3). Python 3.9, standard library only.

Syntax: {{section.key}}, {{section.key | list}}, and line-level blocks {{#if facts.name}} ... {{/if}}.
Fill is single pass: an inserted value is never scanned again. Unfilled placeholders stay as written and are reported."""
import configparser
import csv
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


# ---- value sources (spec §3.2): profile.ini, then mapped site.conf keys, then defaults.ini (decision.* only) ----
SECRET = re.compile(r"(?i)(password|passphrase|secret|token|BEGIN .*PRIVATE)|^[A-Za-z0-9+/=]{32,}$")
TRUE, FALSE = {"yes", "true", "1"}, {"no", "false", "0"}
DEFAULT = "default (not yet confirmed)"


def _read(path):
    return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def _ini(path):
    cp = configparser.ConfigParser(interpolation=None, strict=True)
    try:
        cp.read_string(_read(path), source=str(path))
    except configparser.Error as e:
        raise FillError(f"{path}:{getattr(e, 'lineno', 0)}: {e.__class__.__name__}") from None
    out = {}
    for sec in cp.sections():
        for opt, raw in cp.items(sec):
            lines = [x.strip() for x in raw.split("\n") if x.strip()]
            is_list = raw.startswith("\n") or "\n" in raw.strip()   # a value written on following lines is a list
            out[f"{sec.lower()}.{opt}"] = lines if is_list else raw.strip()
    return out


def _check_secret(path, key, value):
    for item in (value if isinstance(value, list) else [value]):
        if SECRET.search(item):
            raise FillError(f"{path}: {key}: looks like a secret; secrets never go in a profile")


def _site_conf(path):
    kv = {}
    for n, line in enumerate(_read(path).split("\n"), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "=" not in s:
            raise FillError(f"{path}:{n}: expected KEY=VALUE")
        k, v = s.split("=", 1)
        kv[k.strip()] = v.strip()
    return kv


def load_mapping(path):
    with open(path, encoding="utf-8") as f:
        return {r["site_conf_key"]: (r["placeholder"], r["visibility"]) for r in csv.DictReader(f)}


def load_values(profile, site_conf, defaults, mapping):
    """Return (values, facts, provenance). Facts are the [facts] section as booleans."""
    values, facts, prov = {}, {}, {}
    if profile:
        for key, val in _ini(profile).items():
            _check_secret(profile, key, val)
            if key.startswith("facts."):
                v = (val if isinstance(val, str) else "").lower()
                if v not in TRUE | FALSE:
                    raise FillError(f"{profile}: {key}: must be yes or no")
                facts[key] = v in TRUE
            else:
                values[key], prov[key] = val, "profile"
    if site_conf:
        kv = _site_conf(site_conf)
        for sc_key, (placeholder, _vis) in load_mapping(mapping).items():
            if sc_key in kv and placeholder not in values:
                values[placeholder], prov[placeholder] = kv[sc_key], "site.conf"
    if defaults:
        for key, val in _ini(defaults).items():
            if key.startswith("decision.") and key not in values:
                values[key], prov[key] = val, DEFAULT
    return values, facts, prov


# ---- vocabulary and visibility (spec §3.3) ----
VOCAB_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*(\w+)\s*\|\s*([\w-]+)\s*\|\s*(.+?)\s*\|\s*$")
SEGMENT = {"<n>": r"[0-9]+", "<name>": r"[a-z][a-z0-9_]*"}


def load_vocabulary(path):
    """{placeholder: {kind, visibility, meaning, regex}} from vocabulary.md's table."""
    out = {}
    for line in _read(path).split("\n"):
        m = VOCAB_ROW.match(line)
        if not m or m.group(1) == "placeholder":
            continue
        name = m.group(1)
        rx = "^" + r"\.".join(SEGMENT.get(seg, re.escape(seg)) for seg in name.split(".")) + "$"
        out[name] = {"kind": m.group(2), "visibility": m.group(3), "meaning": m.group(4), "regex": re.compile(rx)}
    return out


def vocab_entry(key, vocab):
    if key in vocab:
        return vocab[key]
    for row in vocab.values():
        if row["regex"].match(key):
            return row
    return None


def check_values(values, facts, vocab, public):
    """Every supplied key must be in the vocabulary; in a public copy, no private or never-to-ai value is placed."""
    for key in list(values) + list(facts):
        row = vocab_entry(key, vocab)
        if row is None:
            raise FillError(f"{key} is not in vocabulary.md (add it there first)")
        if public and key in values and row["visibility"] != "public":
            raise FillError(f"{key} is {row['visibility']}: not placed in a public copy")
