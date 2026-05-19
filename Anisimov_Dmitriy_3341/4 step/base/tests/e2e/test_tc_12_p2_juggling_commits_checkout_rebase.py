import pytest


@pytest.mark.positive
def test_tc_12_p2_juggling_commits_rebases_main_after_checkout(lgb):
    lgb.open_level("mixed2")

    commands = [
        ("interactive", "HEAD~2", ["C3", "C2"]),
        "git commit --amend",
        ("interactive", "HEAD~2", ["C2''", "C3'"]),
        "git checkout main",
        "git rebase caption",
    ]
    results = [
        lgb.interactive_rebase(command[1], command[2])
        if isinstance(command, tuple)
        else lgb.run(command)
        for command in commands
    ]
    lgb.wait_for_level_success("mixed2")

    graph = lgb.svg_text()
    assert all(not result["error"] for result in results)
    assert "main" in graph
    assert "caption" in graph
    assert lgb.is_level_solved("mixed2")
