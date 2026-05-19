import pytest


@pytest.mark.negative
def test_tc_14_n2_tags_wrong_v1_target_not_solved(lgb):
    lgb.open_level("mixed4")

    results = [
        lgb.run("git tag v1 side"),
        lgb.run("git tag v0 main~2"),
        lgb.run("git checkout v1"),
    ]

    graph = lgb.svg_text()
    assert all(not result["error"] for result in results)
    assert "v1" in graph
    assert "v0" in graph
    assert not lgb.is_level_solved("mixed4")
