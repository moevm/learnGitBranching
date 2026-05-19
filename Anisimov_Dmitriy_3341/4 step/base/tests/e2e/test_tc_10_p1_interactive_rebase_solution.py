import pytest


@pytest.mark.positive
def test_tc_10_p1_interactive_rebase_reorders_commits(lgb):
    lgb.open_level("move2")
    before_graph = lgb.svg_text()

    command = lgb.interactive_rebase("overHere", ["C3", "C5", "C4"])
    lgb.wait_for_level_success("move2")

    after_graph = lgb.svg_text()
    assert not command["error"]
    assert after_graph != before_graph
    assert "main" in after_graph
    assert "HEAD" in after_graph
    assert lgb.is_level_solved("move2")
