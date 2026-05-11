import pytest


@pytest.mark.negative
def test_tc_05_n_checkout_branch_does_not_detach_head(lgb):
    lgb.open_level("rampup1")
    before_graph = lgb.svg_text()

    checkout_command = lgb.run("git checkout bugFix")

    assert not checkout_command["error"]
    assert lgb.svg_text() == before_graph
    assert not lgb.is_level_solved("rampup1")
