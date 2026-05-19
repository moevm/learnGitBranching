import pytest


@pytest.mark.positive
def test_tc_14_p1_tags_solution_with_relative_refs(lgb):
    lgb.open_level("mixed4")

    commands = [
        "git tag v1 side~1",
        "git tag v0 main~2",
        "git checkout v1",
    ]
    results = [lgb.run(command) for command in commands]
    lgb.wait_for_level_success("mixed4")

    graph = lgb.svg_text()
    assert all(not result["error"] for result in results)
    assert "v1" in graph
    assert "v0" in graph
    assert "HEAD" in graph
    assert lgb.is_level_solved("mixed4")
