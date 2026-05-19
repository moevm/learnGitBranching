import pytest


@pytest.mark.positive
def test_tc_16_p1_many_rebases_solution_with_branch_arguments(lgb):
    lgb.open_level("advanced1")

    commands = [
        "git rebase main bugFix",
        "git rebase bugFix side",
        "git rebase side another",
        "git rebase another main",
    ]
    results = [lgb.run(command) for command in commands]
    lgb.wait_for_level_success("advanced1")

    graph = lgb.svg_text()
    assert all(not result["error"] for result in results)
    assert "main" in graph
    assert "bugFix" in graph
    assert "side" in graph
    assert "another" in graph
    assert lgb.is_level_solved("advanced1")
