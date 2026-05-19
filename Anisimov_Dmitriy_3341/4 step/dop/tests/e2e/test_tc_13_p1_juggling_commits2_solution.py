import pytest


@pytest.mark.positive
def test_tc_13_p1_juggling_commits2_solution_with_commit_ids(lgb):
    lgb.open_level("mixed3")

    commands = [
        "git checkout main",
        "git cherry-pick C2",
        "git commit --amend",
        "git cherry-pick C3",
    ]
    results = [lgb.run(command) for command in commands]
    lgb.wait_for_level_success("mixed3")

    graph = lgb.svg_text()
    assert all(not result["error"] for result in results)
    assert "main" in graph
    assert "newImage" in graph
    assert "caption" in graph
    assert lgb.is_level_solved("mixed3")
