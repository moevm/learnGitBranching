import pytest


@pytest.mark.positive
def test_tc_07_p2_branch_force_moves_pointer_without_deleting_history(lgb):
    lgb.open_level("rampup3")

    branch_command = lgb.run("git branch -f main C6")

    after_graph = lgb.svg_text()
    assert not branch_command["error"]
    assert branch_command["raw"] == "git branch -f main C6"
    assert "main" in after_graph
    assert "bugFix" in after_graph
    for commit_id in ["C0", "C1", "C2", "C3", "C4", "C5", "C6"]:
        assert commit_id in after_graph
