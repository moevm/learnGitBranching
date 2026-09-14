import pytest


LEVEL_ID = "rampup/cherryPick"


class TestLevel09CherryPick:
    @pytest.mark.positive
    def test_tc_09_p1_solution_in_one_command(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = git_page.run_many(("git cherry-pick C3 C4 C7",))
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.positive
    def test_tc_09_p2_solution_in_separate_commands(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = git_page.run_many(
            ("git cherry-pick C3", "git cherry-pick C4", "git cherry-pick C7")
        )
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.negative
    def test_tc_09_n1_missing_commit_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.run("git cherry-pick C3 C4")
        assert not git_page.is_level_solved(LEVEL_ID)

    @pytest.mark.negative
    def test_tc_09_n2_unknown_commit_returns_error(self, git_page):
        git_page.open_level(LEVEL_ID)
        result = git_page.run("git cherry-pick C99")
        assert result.failed
        assert not git_page.is_level_solved(LEVEL_ID)
