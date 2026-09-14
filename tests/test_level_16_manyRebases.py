LEVEL_ID = "rebase/manyRebases"
SOLUTION = "git rebase main bugFix;git rebase bugFix side;git rebase side another;git rebase another main"


class TestLevel16ManyRebases:
    def test_solution_command(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.enter_solution(SOLUTION)
        assert git_page.wait_for_level_solved(timeout=30)

    def test_hint_available(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.enter_command("hint")
        assert git_page.has_hint_output()

    def test_show_goal(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.enter_command("show goal")
        assert git_page.has_goal_window()

    def test_cherry_pick_disabled(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.enter_command("git cherry-pick C1")
        output = git_page.get_terminal_output().lower()
        assert "disabled" in output or "запрещ" in output or "not allowed" in output

    def test_invalid_command(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.enter_command("git invalidcommand123")
        assert git_page.has_error_output()

    def test_reset_after_progress(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.enter_command("git rebase main bugFix")
        git_page.enter_command("reset")
        assert not git_page.is_level_solved()