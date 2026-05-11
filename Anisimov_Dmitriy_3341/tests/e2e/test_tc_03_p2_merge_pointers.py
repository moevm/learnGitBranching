import pytest


@pytest.mark.positive
def test_tc_03_p2_merge_keeps_bugfix_pointer_visible(lgb):
    lgb.open_level("intro3")
    lgb.run("git branch bugFix")
    lgb.run("git checkout bugFix")
    lgb.run("git commit")
    graph_before_merge = lgb.svg_text()
    lgb.run("git checkout main")
    lgb.run("git commit")

    merge_command = lgb.run("git merge bugFix")
    lgb.wait_for_level_success("intro3")

    graph_after_merge = lgb.svg_text()
    assert not merge_command["error"]
    assert graph_after_merge != graph_before_merge
    assert "bugFix" in graph_after_merge
    assert "main" in graph_after_merge
    assert "HEAD" in graph_after_merge
