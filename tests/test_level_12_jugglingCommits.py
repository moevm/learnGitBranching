import pytest


LEVEL_ID = "mixed/jugglingCommits"


def apply_commit_edit(git_page):
    results = [git_page.interactive_rebase("HEAD~2", ("C3", "C2"))]
    results.append(git_page.run("git commit --amend"))
    results.append(git_page.interactive_rebase("HEAD~2", ("C2''", "C3'")))
    return results


class TestLevel12JugglingCommits:
    @pytest.mark.positive
    def test_tc_12_p1_solution_with_explicit_destination(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = apply_commit_edit(git_page)
        results.append(git_page.run("git rebase caption main"))
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.positive
    def test_tc_12_p2_solution_after_checkout(self, git_page):
        git_page.open_level(LEVEL_ID)
        results = apply_commit_edit(git_page)
        results.extend(git_page.run_many(("git checkout main", "git rebase caption")))
        git_page.wait_for_level_success(LEVEL_ID)
        assert not any(result.failed for result in results)

    @pytest.mark.negative
    def test_tc_12_n1_amending_wrong_commit_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.run("git commit --amend")
        assert not git_page.is_level_solved(LEVEL_ID)

    @pytest.mark.negative
    def test_tc_12_n2_unchanged_order_does_not_solve_level(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.interactive_rebase("HEAD~2", ("C2", "C3"))
        assert not git_page.is_level_solved(LEVEL_ID)
