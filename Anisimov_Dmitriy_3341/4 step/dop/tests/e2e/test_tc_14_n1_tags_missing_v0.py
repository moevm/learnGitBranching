import pytest


@pytest.mark.negative
def test_tc_14_n1_tags_missing_v0_not_solved(lgb):
    lgb.open_level("mixed4")

    tag_command = lgb.run("git tag v1 side~1")
    checkout_command = lgb.run("git checkout v1")

    graph = lgb.svg_text()
    assert not tag_command["error"]
    assert not checkout_command["error"]
    assert "v1" in graph
    assert "v0" not in graph
    assert not lgb.is_level_solved("mixed4")
