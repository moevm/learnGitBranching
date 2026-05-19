import pytest


@pytest.mark.positive
def test_tc_14_p2_tags_solution_with_commit_ids(lgb):
    lgb.open_level("mixed4")

    commands = [
        "git tag v1 C2",
        "git tag v0 C1",
        "git checkout v1",
    ]
    results = [lgb.run(command) for command in commands]
    lgb.wait_for_level_success("mixed4")

    graph = lgb.svg_text()
    assert all(not result["error"] for result in results)
    assert "v1" in graph
    assert "v0" in graph
    assert lgb.is_level_solved("mixed4")
