import pytest


@pytest.mark.negative
def test_tc_12_n1_amending_caption_commit_is_wrong_target(lgb):
    lgb.open_level("mixed2")

    command = lgb.run("git commit --amend")

    graph = lgb.svg_text()
    assert not command["error"]
    assert "caption" in graph
    assert not lgb.is_level_solved("mixed2")
