import pytest


LEVEL_ID = "mixed/jugglingCommits2"


class TestLevel13JugglingCommits2:
    @pytest.mark.positive
    def test_tc_13_p1_solution_with_commit_ids(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = git_page.run_many(
            (
                "git checkout main",
                "git cherry-pick C2",
                "git commit --amend",
                "git cherry-pick C3",
            )
        )
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.positive
    def test_tc_13_p2_solution_with_branch_references(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = git_page.run_many(
            (
                "git checkout main",
                "git cherry-pick newImage",
                "git commit --amend",
                "git cherry-pick caption",
            )
        )
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.negative
    def test_tc_13_n1_missing_amend_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.run_many(
            ("git checkout main", "git cherry-pick C2", "git cherry-pick C3")
        )
        assert not git_page.is_level_solved(LEVEL_ID)

    @pytest.mark.negative
    def test_tc_13_n2_incomplete_commit_set_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.run_many(("git checkout main", "git cherry-pick C3"))
        assert not git_page.is_level_solved(LEVEL_ID)
