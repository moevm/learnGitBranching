import pytest


@pytest.mark.negative
def test_tc_11_n2_rebasing_full_bugfix_history_is_wrong(lgb):
    lgb.open_level("mixed1")

    command = lgb.run("git rebase main")

    graph = lgb.svg_text()
    assert not command["error"]
    assert "bugFix" in graph
    assert "debug" in graph
    assert "printf" in graph
    assert not lgb.is_level_solved("mixed1")
