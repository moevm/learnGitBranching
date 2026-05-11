import pytest


@pytest.mark.positive
def test_tc_04_p1_complete_rebase_level(lgb):
    lgb.open_level("intro4")

    commands = [
        "git branch bugFix",
        "git checkout bugFix",
        "git commit",
        "git checkout main",
        "git commit",
        "git checkout bugFix",
        "git rebase main",
    ]
    results = [lgb.run(command) for command in commands]
    lgb.wait_for_level_success("intro4")

    graph = lgb.svg_text()
    assert all(not result["error"] for result in results)
    assert "bugFix" in graph
    assert "main" in graph
    assert "HEAD" in graph
    assert lgb.is_level_solved("intro4")
