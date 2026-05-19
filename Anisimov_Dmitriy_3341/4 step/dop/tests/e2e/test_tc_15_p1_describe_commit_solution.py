import pytest


@pytest.mark.positive
def test_tc_15_p1_describe_level_commit_solution(lgb):
    lgb.open_level("mixed5")

    command = lgb.run("git commit")
    lgb.wait_for_level_success("mixed5")

    graph = lgb.svg_text()
    assert not command["error"]
    assert "main" in graph
    assert "bugFix" in graph
    assert lgb.is_level_solved("mixed5")
