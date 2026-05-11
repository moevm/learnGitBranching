import pytest


@pytest.mark.positive
def test_tc_06_p2_checkout_bugfix_parent_with_tilde(lgb):
    lgb.open_level("rampup2")
    before_graph = lgb.svg_text()

    checkout_command = lgb.run("git checkout bugFix~1")
    lgb.wait_for_level_success("rampup2")

    after_graph = lgb.svg_text()
    assert not checkout_command["error"]
    assert after_graph != before_graph
    assert "bugFix" in after_graph
    assert "HEAD" in after_graph
    assert lgb.is_level_solved("rampup2")
