import pytest


@pytest.mark.positive
def test_tc_15_p2_describe_command_then_commit_solution(lgb):
    lgb.open_level("mixed5")

    describe_command = lgb.run("git describe")
    commit_command = lgb.run("git commit")
    lgb.wait_for_level_success("mixed5")

    assert "Command Result" in describe_command["error"] or "v" in describe_command["result"]
    assert not commit_command["error"]
    assert lgb.terminal_output().strip()
    assert lgb.is_level_solved("mixed5")
