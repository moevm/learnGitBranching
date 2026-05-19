import pytest


@pytest.mark.negative
def test_tc_09_n2_cherry_pick_unknown_commit_keeps_level_unsolved(lgb):
    lgb.open_level("move1")
    before_graph = lgb.svg_text()

    command = lgb.run("git cherry-pick C99")

    assert command["error"] or "C99" in command["result"]
    assert lgb.svg_text() == before_graph
    assert not lgb.is_level_solved("move1")
