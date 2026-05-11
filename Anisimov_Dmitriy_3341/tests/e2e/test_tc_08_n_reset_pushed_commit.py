import pytest


@pytest.mark.negative
def test_tc_08_n_reset_pushed_commit_is_wrong_strategy(lgb):
    lgb.open_level("rampup4")
    checkout_command = lgb.run("git checkout pushed")

    reset_command = lgb.run("git reset HEAD~1")

    graph = lgb.svg_text()
    assert not checkout_command["error"]
    assert reset_command["error"] or not lgb.is_level_solved("rampup4")
    assert "pushed" in graph
    assert not lgb.is_level_solved("rampup4")
