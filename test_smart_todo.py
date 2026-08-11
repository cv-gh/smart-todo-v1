from datetime import date, timedelta
import unittest

from smart_todo import SmartTodoApp, Todo


class SmartTodoAppTests(unittest.TestCase):
    def test_due_today_is_prioritized(self) -> None:
        app = SmartTodoApp()
        today = date(2026, 1, 10)
        app.add_todo(Todo(title="Write docs", due_date=today + timedelta(days=3)))
        app.add_todo(Todo(title="Update urgent release notes", due_date=today))

        suggestion = app.suggest_next(today=today)

        self.assertIsNotNone(suggestion)
        self.assertEqual("Update urgent release notes", suggestion.title)

    def test_focus_tag_boosts_matching_todo(self) -> None:
        app = SmartTodoApp()
        today = date(2026, 1, 10)
        app.add_todo(Todo(title="Refactor API", tags=["engineering"]))
        app.add_todo(Todo(title="Plan roadmap", tags=["product"]))

        suggestion = app.suggest_next(focus_tags=["product"], today=today)

        self.assertIsNotNone(suggestion)
        self.assertEqual("Plan roadmap", suggestion.title)

    def test_add_todo_from_text_parses_due_date_tags_and_estimate(self) -> None:
        app = SmartTodoApp()
        today = date(2026, 1, 10)

        todo = app.add_todo_from_text("Prepare sprint plan tomorrow #work 2h", today=today)

        self.assertEqual(today + timedelta(days=1), todo.due_date)
        self.assertEqual(["work"], todo.tags)
        self.assertEqual(120, todo.estimate_minutes)

    def test_completed_todos_are_not_suggested(self) -> None:
        app = SmartTodoApp()
        today = date(2026, 1, 10)
        done = Todo(title="Urgent done task", due_date=today)
        done.completed = True
        app.add_todo(done)
        app.add_todo(Todo(title="Active task"))

        suggestion = app.suggest_next(today=today)

        self.assertIsNotNone(suggestion)
        self.assertEqual("Active task", suggestion.title)


if __name__ == "__main__":
    unittest.main()
