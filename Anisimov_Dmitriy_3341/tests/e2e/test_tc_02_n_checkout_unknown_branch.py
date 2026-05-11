import pytest


@pytest.mark.negative
def test_tc_02_n_checkout_unknown_branch_keeps_graph_unchanged(lgb):
    lgb.open_level("intro2")
    before_graph = lgb.svg_text()

    command = lgb.run("git checkout wrongName")

    assert command["error"] or "wrongName" in command["result"]
    assert lgb.svg_text() == before_graph
    assert not lgb.is_level_solved("intro2")
