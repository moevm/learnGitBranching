import pytest


@pytest.mark.positive
def test_tc_02_p2_checkout_created_branch_completes_level(lgb):
    lgb.open_level("intro2")

    branch_command = lgb.run("git branch bugFix")
    checkout_command = lgb.run("git checkout bugFix")
    lgb.wait_for_level_success("intro2")

    graph = lgb.svg_text()
    assert not branch_command["error"]
    assert not checkout_command["error"]
    assert "bugFix" in graph
    assert "HEAD" in graph
