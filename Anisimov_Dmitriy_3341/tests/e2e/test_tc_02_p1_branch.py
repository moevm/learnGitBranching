import pytest


@pytest.mark.positive
def test_tc_02_p1_branch_command_creates_bugfix_branch(lgb):
    lgb.open_level("intro2")
    before_graph = lgb.svg_text()

    command = lgb.run("git branch bugFix")

    after_graph = lgb.svg_text()
    assert not command["error"]
    assert after_graph != before_graph
    assert "bugFix" in after_graph
    assert "main" in after_graph
