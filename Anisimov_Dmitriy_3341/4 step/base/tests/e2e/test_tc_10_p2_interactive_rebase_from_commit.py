import pytest


@pytest.mark.positive
def test_tc_10_p2_interactive_rebase_uses_equivalent_base_commit(lgb):
    lgb.open_level("move2")

    command = lgb.interactive_rebase("C1", ["C3", "C5", "C4"])
    lgb.wait_for_level_success("move2")

    graph = lgb.svg_text()
    assert not command["error"]
    assert "main" in graph
    assert "HEAD" in graph
    assert lgb.is_level_solved("move2")
