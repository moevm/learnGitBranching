import pytest


@pytest.mark.negative
def test_tc_12_n2_wrong_interactive_rebase_order_not_solved(lgb):
    lgb.open_level("mixed2")

    command = lgb.interactive_rebase("HEAD~2", ["C2", "C3"])

    graph = lgb.svg_text()
    assert not command["error"]
    assert "caption" in graph
    assert "newImage" in graph
    assert not lgb.is_level_solved("mixed2")
