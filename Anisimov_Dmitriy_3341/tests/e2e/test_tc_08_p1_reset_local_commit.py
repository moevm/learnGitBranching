import pytest


@pytest.mark.positive
def test_tc_08_p1_reset_last_local_commit(lgb):
    lgb.open_level("rampup4")
    before_graph = lgb.svg_text()

    reset_command = lgb.run("git reset HEAD~1")

    after_graph = lgb.svg_text()
    assert not reset_command["error"]
    assert after_graph != before_graph
    assert "local" in after_graph
    assert "pushed" in after_graph
    assert "main" in after_graph
