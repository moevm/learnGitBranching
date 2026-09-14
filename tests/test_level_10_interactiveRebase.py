import pytest


LEVEL_ID = "rampup/interactiveRebase"


class TestLevel10InteractiveRebase:
    @pytest.mark.positive
    def test_tc_10_p1_solution_from_named_base(self, git_page):
        git_page.open_level(LEVEL_ID)
        result = git_page.interactive_rebase("overHere", ("C3", "C5", "C4"))
        git_page.wait_for_level_success(LEVEL_ID)
        assert not result.failed

    @pytest.mark.positive
    def test_tc_10_p2_solution_from_commit_reference(self, git_page):
        git_page.open_level(LEVEL_ID)
        result = git_page.interactive_rebase("C1", ("C3", "C5", "C4"))
        git_page.wait_for_level_success(LEVEL_ID)
        assert not result.failed

    @pytest.mark.negative
    def test_tc_10_n1_wrong_order_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.interactive_rebase("overHere", ("C4", "C5", "C3"))
        assert not git_page.is_level_solved(LEVEL_ID)

    @pytest.mark.negative
    def test_tc_10_n2_unknown_base_returns_error(self, git_page):
        git_page.open_level(LEVEL_ID)
        result = git_page.run(
            "git rebase -i wrongBranch --solution-ordering C3,C5,C4"
        )
        assert result.failed
        assert not git_page.is_level_solved(LEVEL_ID)
