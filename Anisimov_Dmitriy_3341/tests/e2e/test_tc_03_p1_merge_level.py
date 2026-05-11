import pytest


@pytest.mark.positive
def test_tc_03_p1_complete_merge_level_from_main(lgb):
    lgb.open_level("intro3")

    commands = [
        "git branch bugFix",
        "git checkout bugFix",
        "git commit",
        "git checkout main",
        "git commit",
        "git merge bugFix",
    ]
    results = [lgb.run(command) for command in commands]
    lgb.wait_for_level_success("intro3")

    graph = lgb.svg_text()
    assert all(not result["error"] for result in results)
    assert "bugFix" in graph
    assert "main" in graph
    assert "HEAD" in graph
    assert lgb.is_level_solved("intro3")
