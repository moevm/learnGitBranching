import pytest


@pytest.mark.positive
def test_tc_09_p1_cherry_pick_required_commits_in_one_command(lgb):
    lgb.open_level("move1")
    before_graph = lgb.svg_text()

    command = lgb.run("git cherry-pick C3 C4 C7")
    lgb.wait_for_level_success("move1")

    after_graph = lgb.svg_text()
    assert not command["error"]
    assert after_graph != before_graph
    assert "main" in after_graph
    assert "HEAD" in after_graph
    assert lgb.is_level_solved("move1")
