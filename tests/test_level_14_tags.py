LEVEL_ID = "mixed/tags"
SOLUTION = "git tag v1 side~1;git tag v0 main~2;git checkout v1"


class TestLevel14Tags:
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

    def test_detached_head_after_tag_checkout(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.enter_command("git tag v1 side~1")
        git_page.enter_command("git tag v0 main~2")
        git_page.enter_command("git checkout v1")
        output = git_page.get_terminal_output().lower()
        assert "detached" in output or "отсоедин" in output or "head" in output

    def test_invalid_command(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.enter_command("git invalidcommand123")
        assert git_page.has_error_output()

    def test_reset_after_progress(self, git_page):
        git_page.open_level(LEVEL_ID)
        git_page.enter_command("git tag v1 side~1")
        git_page.enter_command("reset")
        assert not git_page.is_level_solved()