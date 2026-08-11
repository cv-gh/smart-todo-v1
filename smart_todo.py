from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
import re


@dataclass
class Todo:
    title: str
    due_date: date | None = None
    tags: list[str] = field(default_factory=list)
    estimate_minutes: int = 30
    completed: bool = False


class SmartTodoApp:
    """AI-inspired todo prioritization with lightweight natural-language parsing."""

    _KEYWORD_WEIGHTS = {
        "urgent": 35,
        "asap": 25,
        "important": 20,
        "blocked": 20,
        "bug": 15,
        "meeting": 10,
    }

    def __init__(self) -> None:
        self.todos: list[Todo] = []

    def add_todo(self, todo: Todo) -> None:
        self.todos.append(todo)

    def add_todo_from_text(self, text: str, today: date | None = None) -> Todo:
        parsed_today = today or date.today()
        due_date = self._extract_due_date(text, parsed_today)
        tags = [match.lower() for match in re.findall(r"#([A-Za-z0-9_-]+)", text)]
        estimate = self._extract_estimate_minutes(text)
        title = text.strip()
        if not title:
            raise ValueError("todo text cannot be empty")
        todo = Todo(title=title, due_date=due_date, tags=tags, estimate_minutes=estimate)
        self.add_todo(todo)
        return todo

    def suggest_next(
        self, focus_tags: list[str] | None = None, today: date | None = None
    ) -> Todo | None:
        candidates = [todo for todo in self.todos if not todo.completed]
        if not candidates:
            return None
        normalized_focus_tags = {tag.lower() for tag in (focus_tags or [])}
        score_date = today or date.today()
        return max(
            candidates,
            key=lambda todo: self._score_todo(
                todo=todo, focus_tags=normalized_focus_tags, today=score_date
            ),
        )

    def complete_todo(self, title: str) -> bool:
        for todo in self.todos:
            if todo.title == title:
                todo.completed = True
                return True
        return False

    def _score_todo(self, todo: Todo, focus_tags: set[str], today: date) -> int:
        score = 0
        if todo.due_date is not None:
            days_until_due = (todo.due_date - today).days
            if days_until_due < 0:
                score += 120
            elif days_until_due == 0:
                score += 100
            elif days_until_due <= 3:
                score += 70 - (days_until_due * 10)
            elif days_until_due <= 7:
                score += 30
            else:
                score += 10

        title_lower = todo.title.lower()
        for keyword, weight in self._KEYWORD_WEIGHTS.items():
            if keyword in title_lower:
                score += weight

        if todo.estimate_minutes <= 15:
            score += 15
        elif todo.estimate_minutes <= 30:
            score += 8
        elif todo.estimate_minutes >= 120:
            score -= 10

        if focus_tags and focus_tags.intersection({tag.lower() for tag in todo.tags}):
            score += 20
        return score

    @staticmethod
    def _extract_due_date(text: str, today: date) -> date | None:
        lowered = text.lower()
        if "today" in lowered:
            return today
        if "tomorrow" in lowered:
            return today + timedelta(days=1)
        match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", text)
        if not match:
            return None
        return date.fromisoformat(match.group(1))

    @staticmethod
    def _extract_estimate_minutes(text: str) -> int:
        match = re.search(
            r"\b(\d+)\s*(m|min|mins|minute|minutes|h|hr|hrs|hour|hours)\b",
            text.lower(),
        )
        if not match:
            return 30
        amount = int(match.group(1))
        unit = match.group(2)
        if unit.startswith("h"):
            return amount * 60
        return amount
