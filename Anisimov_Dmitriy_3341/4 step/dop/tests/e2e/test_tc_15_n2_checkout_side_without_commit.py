import pytest


@pytest.mark.negative
def test_tc_15_n2_checkout_side_without_commit_not_solved(lgb):
    lgb.open_level("mixed5")

    command = lgb.run("git checkout side")

    graph = lgb.svg_text()
    assert not command["error"]
    assert "side" in graph
    assert not lgb.is_level_solved("mixed5")
