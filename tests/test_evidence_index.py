from pathlib import Path

from tools.evidence_index import index

XCCDF = """<?xml version="1.0"?>
<Benchmark xmlns="http://checklists.nist.gov/xccdf/1.2" id="b">
  <Rule id="r_pass"><title>Rule that passes</title>
    <reference href="https://doi.org/10.6028/NIST.SP.800-171">3.1.1,3.1.2</reference></Rule>
  <Rule id="r_fail"><title>Rule that fails</title>
    <reference href="https://doi.org/10.6028/NIST.SP.800-171">3.1.1</reference></Rule>
  <Rule id="r_other"><title>Not 800-171</title><reference href="https://example.test/other">9.9</reference></Rule>
  <TestResult id="t">
    <rule-result idref="r_pass"><result>pass</result></rule-result>
    <rule-result idref="r_fail"><result>fail</result></rule-result>
    <rule-result idref="r_other"><result>pass</result></rule-result>
  </TestResult>
</Benchmark>"""


def test_index_groups_rules_by_requirement(tmp_path):
    p = tmp_path / "scan.xml"
    p.write_text(XCCDF)
    idx = index([p])
    assert idx["3.1.1"] == {"pass": [("r_pass", "Rule that passes")], "fail": [("r_fail", "Rule that fails")]}
    assert idx["3.1.2"]["pass"] == [("r_pass", "Rule that passes")] and "9.9" not in idx
