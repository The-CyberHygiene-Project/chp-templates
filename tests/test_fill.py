import pytest
from render.chpfill import FillError, fill_text


def test_value_list_and_unfilled():
    out, unfilled = fill_text("A {{org.name}}\n{{org.reviewers | list}}\nB {{org.missing}}\n",
                              {"org.name": "Example Manufacturing LLC", "org.reviewers": ["Smith, J.", "Lee, K."]}, {}, "t.md")
    assert out == "A Example Manufacturing LLC\n- Smith, J.\n- Lee, K.\nB {{org.missing}}\n"
    assert unfilled == [("org.missing", 3)]


def test_list_items_keep_their_commas():
    out, _ = fill_text("{{a.b | list}}", {"a.b": ["Smith, J."]}, {}, "t.md")
    assert out == "- Smith, J."


def test_value_with_braces_is_inserted_literally():
    out, unfilled = fill_text("{{a.b}}", {"a.b": "{{x.y}} Co"}, {}, "t.md")
    assert out == "{{x.y}} Co" and unfilled == []


def test_if_true_false_and_not_applicable():
    t = "{{#if facts.has_wireless}}\nWireless text.\n{{/if}}\n"
    assert fill_text(t, {}, {"facts.has_wireless": True}, "t.md")[0] == "Wireless text.\n"
    out, _ = fill_text(t, {}, {"facts.has_wireless": False}, "t.md")
    assert out == "*Not applicable: facts.has_wireless = no.*\n"


def test_unknown_fact_leaves_block_and_reports():
    t = "{{#if facts.x}}\nT\n{{/if}}\n"
    out, unfilled = fill_text(t, {}, {}, "t.md")
    assert "{{#if facts.x}}" in out and ("facts.x", 1) in unfilled


@pytest.mark.parametrize("t,line", [("{{#if facts.a}}\nx\n", 1), ("x\n{{/if}}\n", 2),
                                    ("{{#if facts.a}}\n{{#if facts.b}}\n{{/if}}\n", 2), ("{{a.b | lisst}}", 1)])
def test_unclosed_if_is_an_error_with_line(t, line):
    with pytest.raises(FillError, match=rf"^t\.md:{line}: "):
        fill_text(t, {}, {"facts.a": True, "facts.b": True}, "t.md")


def test_a_bad_filter_in_a_skipped_block_is_still_an_error():
    with pytest.raises(FillError, match=r"^t\.md:2: unknown filter"):
        fill_text("{{#if facts.a}}\n{{x.y | bad}}\n{{/if}}\n", {}, {"facts.a": False}, "t.md")
