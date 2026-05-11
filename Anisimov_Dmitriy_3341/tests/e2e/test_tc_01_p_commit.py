import pytest


@pytest.mark.positive
def test_tc_01_p_commit_completes_intro_level(lgb):
    lgb.open_level("intro1")
    before_graph = lgb.svg_text()

    first_commit = lgb.run("git commit")
    second_commit = lgb.run("git commit")
    lgb.wait_for_level_success("intro1")

    after_graph = lgb.svg_text()
    assert not first_commit["error"]
    assert not second_commit["error"]
    assert after_graph != before_graph
    assert "C2" in after_graph
    assert "C3" in after_graph
    assert "main" in after_graph
    assert "HEAD" in after_graph
