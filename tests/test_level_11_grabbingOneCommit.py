import pytest


LEVEL_ID = "mixed/grabbingOneCommit"


class TestLevel11GrabbingOneCommit:
    @pytest.mark.positive
    def test_tc_11_p1_solution_with_interactive_rebase(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = [git_page.interactive_rebase("main", ("C4",))]
        results.append(git_page.run("git rebase bugFix main"))
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.positive
    def test_tc_11_p2_solution_with_cherry_pick(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = git_page.run_many(("git checkout main", "git cherry-pick bugFix"))
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.negative
    def test_tc_11_n1_wrong_commit_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.run_many(("git checkout main", "git cherry-pick debug"))
        assert not git_page.is_level_solved(LEVEL_ID)

    @pytest.mark.negative
    def test_tc_11_n2_full_rebase_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.run("git rebase main")
        assert not git_page.is_level_solved(LEVEL_ID)
