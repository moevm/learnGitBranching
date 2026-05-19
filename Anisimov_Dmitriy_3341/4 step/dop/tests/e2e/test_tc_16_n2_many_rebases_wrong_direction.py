import pytest


@pytest.mark.negative
def test_tc_16_n2_many_rebases_wrong_direction_not_solved(lgb):
    lgb.open_level("advanced1")

    command = lgb.run("git rebase bugFix main")

    graph = lgb.svg_text()
    assert not command["error"]
    assert "main" in graph
    assert "bugFix" in graph
    assert not lgb.is_level_solved("advanced1")
