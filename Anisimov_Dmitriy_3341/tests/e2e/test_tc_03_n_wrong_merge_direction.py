import pytest


@pytest.mark.negative
def test_tc_03_n_merge_from_bugfix_is_wrong_direction(lgb):
    lgb.open_level("intro3")
    lgb.run("git branch bugFix")
    lgb.run("git checkout bugFix")
    lgb.run("git commit")
    lgb.run("git checkout main")
    lgb.run("git commit")
    lgb.run("git checkout bugFix")

    merge_command = lgb.run("git merge main")

    graph = lgb.svg_text()
    assert not merge_command["error"]
    assert "bugFix" in graph
    assert "main" in graph
    assert not lgb.is_level_solved("intro3")
