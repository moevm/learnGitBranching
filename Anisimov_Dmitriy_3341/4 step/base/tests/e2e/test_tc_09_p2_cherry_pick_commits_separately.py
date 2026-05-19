import pytest


@pytest.mark.positive
def test_tc_09_p2_cherry_pick_required_commits_separately(lgb):
    lgb.open_level("move1")

    results = [
        lgb.run("git cherry-pick C3"),
        lgb.run("git cherry-pick C4"),
        lgb.run("git cherry-pick C7"),
    ]
    lgb.wait_for_level_success("move1")

    graph = lgb.svg_text()
    assert all(not result["error"] for result in results)
    assert "main" in graph
    assert "HEAD" in graph
    assert lgb.is_level_solved("move1")
