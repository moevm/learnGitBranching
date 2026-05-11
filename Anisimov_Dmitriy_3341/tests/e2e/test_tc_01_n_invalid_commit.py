import pytest


@pytest.mark.negative
def test_tc_01_n_invalid_commit_command_does_not_change_graph(lgb):
    lgb.open_level("intro1")
    before_graph = lgb.svg_text()

    command = lgb.run("git commmit")

    assert command["error"] or "error" in command["result"].lower()
    assert lgb.svg_text() == before_graph
    assert not lgb.is_level_solved("intro1")
