import pytest


@pytest.mark.negative
def test_tc_11_n1_grabbing_debug_commit_is_not_target_state(lgb):
    lgb.open_level("mixed1")
    lgb.run("git checkout main")

    command = lgb.run("git cherry-pick debug")

    graph = lgb.svg_text()
    assert not command["error"]
    assert "debug" in graph
    assert not lgb.is_level_solved("mixed1")
