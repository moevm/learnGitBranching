import pytest


@pytest.mark.positive
def test_tc_05_p1_checkout_c4_detaches_head(lgb):
    lgb.open_level("rampup1")
    before_graph = lgb.svg_text()

    checkout_command = lgb.run("git checkout C4")
    lgb.wait_for_level_success("rampup1")

    after_graph = lgb.svg_text()
    assert not checkout_command["error"]
    assert after_graph != before_graph
    assert "bugFix" in after_graph
    assert "HEAD" in after_graph
    assert "C4" in after_graph
    assert lgb.is_level_solved("rampup1")
