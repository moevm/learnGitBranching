import pytest


@pytest.mark.positive
def test_tc_05_p2_checkout_other_commit_keeps_detached_head(lgb):
    lgb.open_level("rampup1")
    first_checkout = lgb.run("git checkout C4")
    graph_after_first_checkout = lgb.svg_text()

    second_checkout = lgb.run("git checkout C3")

    graph_after_second_checkout = lgb.svg_text()
    assert not first_checkout["error"]
    assert not second_checkout["error"]
    assert graph_after_second_checkout != graph_after_first_checkout
    assert "bugFix" in graph_after_second_checkout
    assert "HEAD" in graph_after_second_checkout
    assert "C3" in graph_after_second_checkout
