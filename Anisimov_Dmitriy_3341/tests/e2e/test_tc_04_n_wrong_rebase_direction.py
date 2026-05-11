import pytest


@pytest.mark.negative
def test_tc_04_n_rebase_from_main_is_wrong_direction(lgb):
    lgb.open_level("intro4")
    lgb.run("git branch bugFix")
    lgb.run("git checkout bugFix")
    lgb.run("git commit")
    lgb.run("git checkout main")
    lgb.run("git commit")

    rebase_command = lgb.run("git rebase bugFix")

    graph = lgb.svg_text()
    assert not rebase_command["error"]
    assert "bugFix" in graph
    assert "main" in graph
    assert not lgb.is_level_solved("intro4")
