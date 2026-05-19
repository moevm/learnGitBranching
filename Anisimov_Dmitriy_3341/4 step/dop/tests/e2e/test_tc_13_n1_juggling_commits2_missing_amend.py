import pytest


@pytest.mark.negative
def test_tc_13_n1_juggling_commits2_missing_amend_not_solved(lgb):
    lgb.open_level("mixed3")

    lgb.run("git checkout main")
    first_pick = lgb.run("git cherry-pick C2")
    second_pick = lgb.run("git cherry-pick C3")

    assert not first_pick["error"]
    assert not second_pick["error"]
    assert not lgb.is_level_solved("mixed3")
