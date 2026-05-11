import pytest


@pytest.mark.negative
def test_tc_07_n_branch_without_force_does_not_move_existing_branch(lgb):
    lgb.open_level("rampup3")
    before_graph = lgb.svg_text()

    branch_command = lgb.run("git branch main HEAD")

    assert branch_command["error"] or lgb.svg_text() == before_graph
    assert not lgb.is_level_solved("rampup3")
