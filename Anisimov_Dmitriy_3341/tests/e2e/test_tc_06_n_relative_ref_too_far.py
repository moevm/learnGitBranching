import pytest


@pytest.mark.negative
def test_tc_06_n_checkout_parent_too_far_does_not_solve_level(lgb):
    lgb.open_level("rampup2")
    before_graph = lgb.svg_text()

    checkout_command = lgb.run("git checkout bugFix~5")

    assert checkout_command["error"] or not lgb.is_level_solved("rampup2")
    assert lgb.svg_text() == before_graph or not lgb.is_level_solved("rampup2")
    assert not lgb.is_level_solved("rampup2")
