import pytest


@pytest.mark.negative
def test_tc_13_n2_juggling_commits2_wrong_cherry_pick_not_solved(lgb):
    lgb.open_level("mixed3")

    lgb.run("git checkout main")
    command = lgb.run("git cherry-pick C3")

    graph = lgb.svg_text()
    assert not command["error"]
    assert "main" in graph
    assert not lgb.is_level_solved("mixed3")
