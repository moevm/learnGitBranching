import pytest


@pytest.mark.positive
def test_tc_13_p2_juggling_commits2_solution_with_branch_refs(lgb):
    lgb.open_level("mixed3")

    commands = [
        "git checkout main",
        "git cherry-pick newImage",
        "git commit --amend",
        "git cherry-pick caption",
    ]
    results = [lgb.run(command) for command in commands]
    lgb.wait_for_level_success("mixed3")

    graph = lgb.svg_text()
    assert all(not result["error"] for result in results)
    assert "main" in graph
    assert "caption" in graph
    assert lgb.is_level_solved("mixed3")
