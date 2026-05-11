import pytest


@pytest.mark.positive
def test_tc_04_p2_rebase_places_bugfix_after_main_commit(lgb):
    lgb.open_level("intro4")
    lgb.run("git branch bugFix")
    lgb.run("git checkout bugFix")
    lgb.run("git commit")
    lgb.run("git checkout main")
    lgb.run("git commit")
    lgb.run("git checkout bugFix")
    graph_before_rebase = lgb.svg_text()

    rebase_command = lgb.run("git rebase main")
    lgb.wait_for_level_success("intro4")

    graph_after_rebase = lgb.svg_text()
    assert not rebase_command["error"]
    assert graph_after_rebase != graph_before_rebase
    assert "bugFix" in graph_after_rebase
    assert "main" in graph_after_rebase
    assert "HEAD" in graph_after_rebase
    assert lgb.is_level_solved("intro4")
