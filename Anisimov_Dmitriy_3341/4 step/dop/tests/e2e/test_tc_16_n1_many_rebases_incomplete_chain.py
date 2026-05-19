import pytest


@pytest.mark.negative
def test_tc_16_n1_many_rebases_incomplete_chain_not_solved(lgb):
    lgb.open_level("advanced1")

    first = lgb.run("git rebase main bugFix")
    second = lgb.run("git rebase bugFix side")

    graph = lgb.svg_text()
    assert not first["error"]
    assert not second["error"]
    assert "main" in graph
    assert not lgb.is_level_solved("advanced1")
