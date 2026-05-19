import pytest


@pytest.mark.negative
def test_tc_10_n2_interactive_rebase_unknown_base_fails(lgb):
    lgb.open_level("move2")
    before_graph = lgb.svg_text()

    command = lgb.run("git rebase -i wrongBranch --solution-ordering C3,C5,C4")

    assert command["error"] or "wrongBranch" in command["result"]
    assert lgb.svg_text() == before_graph
    assert not lgb.is_level_solved("move2")
