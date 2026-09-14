import pytest


LEVEL_ID = "mixed/tags"


class TestLevel14Tags:
    @pytest.mark.positive
    def test_tc_14_p1_solution_with_relative_references(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = git_page.run_many(
            ("git tag v1 side~1", "git tag v0 main~2", "git checkout v1")
        )
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.positive
    def test_tc_14_p2_solution_with_commit_ids(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = git_page.run_many(
            ("git tag v1 C2", "git tag v0 C1", "git checkout v1")
        )
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.negative
    def test_tc_14_n1_missing_tag_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.run_many(("git tag v1 side~1", "git checkout v1"))
        assert not git_page.is_level_solved(LEVEL_ID)

    @pytest.mark.negative
    def test_tc_14_n2_tag_on_wrong_commit_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.run_many(
            ("git tag v1 side", "git tag v0 main~2", "git checkout v1")
        )
        assert not git_page.is_level_solved(LEVEL_ID)
