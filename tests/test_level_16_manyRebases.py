import pytest


LEVEL_ID = "rebase/manyRebases"


class TestLevel16ManyRebases:
    @pytest.mark.positive
    def test_tc_16_p1_solution_with_explicit_branches(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = git_page.run_many(
            (
                "git rebase main bugFix",
                "git rebase bugFix side",
                "git rebase side another",
                "git rebase another main",
            )
        )
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.positive
    def test_tc_16_p2_solution_with_checkout_flow(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = git_page.run_many(
            (
                "git checkout bugFix",
                "git rebase main",
                "git checkout side",
                "git rebase bugFix",
                "git checkout another",
                "git rebase side",
                "git checkout main",
                "git rebase another",
            )
        )
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.negative
    def test_tc_16_n1_incomplete_chain_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.run_many(("git rebase main bugFix", "git rebase bugFix side"))
        assert not git_page.is_level_solved(LEVEL_ID)

    @pytest.mark.negative
    def test_tc_16_n2_wrong_direction_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.run("git rebase bugFix main")
        assert not git_page.is_level_solved(LEVEL_ID)
