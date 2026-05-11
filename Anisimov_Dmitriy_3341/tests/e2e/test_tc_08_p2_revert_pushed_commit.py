import pytest


@pytest.mark.positive
def test_tc_08_p2_revert_last_pushed_commit(lgb):
    lgb.open_level("rampup4")
    lgb.run("git reset HEAD~1")
    checkout_command = lgb.run("git checkout pushed")

    revert_command = lgb.run("git revert HEAD")
    lgb.wait_for_level_success("rampup4")

    graph = lgb.svg_text()
    assert not checkout_command["error"]
    assert not revert_command["error"]
    assert "local" in graph
    assert "pushed" in graph
    assert "HEAD" in graph
    assert lgb.is_level_solved("rampup4")
