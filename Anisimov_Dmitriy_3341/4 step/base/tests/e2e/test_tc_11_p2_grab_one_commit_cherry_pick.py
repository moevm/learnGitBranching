import pytest


@pytest.mark.positive
def test_tc_11_p2_grab_one_commit_with_cherry_pick(lgb):
    lgb.open_level("mixed1")

    checkout_command = lgb.run("git checkout main")
    cherry_pick_command = lgb.run("git cherry-pick bugFix")
    lgb.wait_for_level_success("mixed1")

    graph = lgb.svg_text()
    assert not checkout_command["error"]
    assert not cherry_pick_command["error"]
    assert "main" in graph
    assert "bugFix" in graph
    assert lgb.is_level_solved("mixed1")
