import pytest


@pytest.mark.positive
def test_tc_11_p1_grab_one_commit_with_interactive_rebase(lgb):
    lgb.open_level("mixed1")

    first_command = lgb.interactive_rebase("main", ["C4"])
    second_command = lgb.run("git rebase bugFix main")
    lgb.wait_for_level_success("mixed1")

    graph = lgb.svg_text()
    assert not first_command["error"]
    assert not second_command["error"]
    assert "main" in graph
    assert "bugFix" in graph
    assert lgb.is_level_solved("mixed1")
