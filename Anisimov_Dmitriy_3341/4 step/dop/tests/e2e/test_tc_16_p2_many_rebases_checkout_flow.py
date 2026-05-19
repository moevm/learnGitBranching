import pytest


@pytest.mark.positive
def test_tc_16_p2_many_rebases_solution_with_checkout_flow(lgb):
    lgb.open_level("advanced1")

    commands = [
        "git checkout bugFix",
        "git rebase main",
        "git checkout side",
        "git rebase bugFix",
        "git checkout another",
        "git rebase side",
        "git checkout main",
        "git rebase another",
    ]
    results = [lgb.run(command) for command in commands]
    lgb.wait_for_level_success("advanced1")

    graph = lgb.svg_text()
    assert all(not result["error"] for result in results)
    assert "main" in graph
    assert "another" in graph
    assert lgb.is_level_solved("advanced1")
