import pytest


@pytest.mark.negative
def test_tc_09_n1_cherry_pick_not_all_required_commits(lgb):
    lgb.open_level("move1")

    command = lgb.run("git cherry-pick C3 C4")

    graph = lgb.svg_text()
    assert not command["error"]
    assert "main" in graph
    assert not lgb.is_level_solved("move1")
