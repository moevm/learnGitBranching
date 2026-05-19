import pytest


@pytest.mark.negative
def test_tc_10_n1_interactive_rebase_wrong_order_not_solved(lgb):
    lgb.open_level("move2")

    command = lgb.interactive_rebase("overHere", ["C4", "C5", "C3"])

    graph = lgb.svg_text()
    assert not command["error"]
    assert "main" in graph
    assert not lgb.is_level_solved("move2")
