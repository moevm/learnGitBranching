import pytest


LEVEL_ID = "mixed/describe"


class TestLevel15Describe:
    @pytest.mark.positive
    def test_tc_15_p1_solution_with_commit(self, git_page):
        git_page.open_level(LEVEL_ID)
        result = git_page.run("git commit")
        git_page.wait_for_level_success(LEVEL_ID)
        assert not result.failed

    @pytest.mark.positive
    def test_tc_15_p2_describe_before_solution(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = git_page.run_many(("git describe", "git commit"))
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.negative
    def test_tc_15_n1_describe_only_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.run("git describe")
        assert not git_page.is_level_solved(LEVEL_ID)

    @pytest.mark.negative
    def test_tc_15_n2_checkout_only_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.run("git checkout side")
        assert not git_page.is_level_solved(LEVEL_ID)
