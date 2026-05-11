import pytest


@pytest.mark.positive
def test_tc_07_p1_move_head_main_and_bugfix_to_targets(lgb):
    lgb.open_level("rampup3")

    commands = [
        "git branch -f main C6",
        "git checkout HEAD~1",
        "git branch -f bugFix HEAD~1",
    ]
    results = [lgb.run(command) for command in commands]
    lgb.wait_for_level_success("rampup3")

    graph = lgb.svg_text()
    assert all(not result["error"] for result in results)
    assert "main" in graph
    assert "bugFix" in graph
    assert "HEAD" in graph
    assert lgb.is_level_solved("rampup3")
