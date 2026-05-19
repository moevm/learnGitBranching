import pytest


@pytest.mark.negative
def test_tc_15_n1_describe_only_does_not_solve_level(lgb):
    lgb.open_level("mixed5")

    command = lgb.run("git describe")

    assert "Command Result" in command["error"] or "v" in command["result"]
    assert lgb.terminal_output().strip()
    assert not lgb.is_level_solved("mixed5")
