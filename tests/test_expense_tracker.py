import json
import pytest
from unittest.mock import patch
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from expense_tracker import (
    ExpenseTracker,
    prompt_add_expense,
    display_all_expenses,
    display_by_category,
    display_summary,
    prompt_delete_expense,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tracker(tmp_path):
    """Fresh ExpenseTracker backed by a temp file."""
    return ExpenseTracker(data_file=str(tmp_path / "expenses.json"))


@pytest.fixture
def populated_tracker(tracker):
    """Tracker with three pre-loaded expenses across two categories."""
    tracker.add(10.00, "Food", "Lunch")
    tracker.add(5.50, "Food", "Coffee")
    tracker.add(20.00, "Transport", "Taxi")
    return tracker


# ---------------------------------------------------------------------------
# ExpenseTracker.add
# ---------------------------------------------------------------------------

class TestAdd:
    def test_returns_expense_dict(self, tracker):
        expense = tracker.add(12.50, "Food", "Lunch")
        assert expense["amount"] == 12.50
        assert expense["category"] == "Food"
        assert expense["description"] == "Lunch"
        assert expense["id"] == 1
        assert "date" in expense

    def test_amount_rounded_to_two_decimals(self, tracker):
        expense = tracker.add(9.999, "Food", "Snack")
        assert expense["amount"] == 10.00

    def test_increments_id(self, tracker):
        e1 = tracker.add(1.00, "A", "first")
        e2 = tracker.add(2.00, "B", "second")
        assert e2["id"] == e1["id"] + 1

    def test_persists_to_file(self, tracker):
        tracker.add(7.00, "Bills", "Internet")
        data = json.loads(Path(tracker.data_file).read_text())
        assert len(data) == 1
        assert data[0]["amount"] == 7.00

    def test_list_grows(self, tracker):
        tracker.add(1.00, "A", "x")
        tracker.add(2.00, "B", "y")
        assert len(tracker.expenses) == 2


# ---------------------------------------------------------------------------
# ExpenseTracker.delete
# ---------------------------------------------------------------------------

class TestDelete:
    def test_delete_existing_returns_true(self, populated_tracker):
        assert populated_tracker.delete(1) is True

    def test_delete_removes_expense(self, populated_tracker):
        populated_tracker.delete(1)
        assert all(e["id"] != 1 for e in populated_tracker.expenses)

    def test_delete_missing_returns_false(self, tracker):
        assert tracker.delete(999) is False

    def test_delete_persists(self, populated_tracker):
        populated_tracker.delete(1)
        data = json.loads(Path(populated_tracker.data_file).read_text())
        assert all(e["id"] != 1 for e in data)

    def test_id_not_reused_while_others_exist(self, tracker):
        # Delete a middle ID — the next add should use max(remaining) + 1, not the gap
        tracker.add(1.00, "A", "first")
        tracker.add(2.00, "B", "second")
        tracker.add(3.00, "C", "third")
        tracker.delete(2)
        e4 = tracker.add(4.00, "D", "fourth")
        assert e4["id"] == 4


# ---------------------------------------------------------------------------
# ExpenseTracker.totals_by_category
# ---------------------------------------------------------------------------

class TestTotalsByCategory:
    def test_sums_correctly(self, populated_tracker):
        totals = populated_tracker.totals_by_category()
        assert totals["Food"] == pytest.approx(15.50)
        assert totals["Transport"] == pytest.approx(20.00)

    def test_empty_tracker(self, tracker):
        assert tracker.totals_by_category() == {}

    def test_single_category(self, tracker):
        tracker.add(3.00, "X", "a")
        tracker.add(7.00, "X", "b")
        assert tracker.totals_by_category()["X"] == pytest.approx(10.00)


# ---------------------------------------------------------------------------
# ExpenseTracker.summary
# ---------------------------------------------------------------------------

class TestSummary:
    def test_returns_none_when_empty(self, tracker):
        assert tracker.summary() is None

    def test_correct_stats(self, populated_tracker):
        stats = populated_tracker.summary()
        assert stats["total"] == pytest.approx(35.50)
        assert stats["count"] == 3
        assert stats["average"] == pytest.approx(35.50 / 3)

    def test_single_expense(self, tracker):
        tracker.add(10.00, "X", "y")
        stats = tracker.summary()
        assert stats["total"] == 10.00
        assert stats["count"] == 1
        assert stats["average"] == 10.00


# ---------------------------------------------------------------------------
# Persistence: load from existing file
# ---------------------------------------------------------------------------

class TestPersistence:
    def test_loads_existing_file(self, tmp_path):
        data = [{"id": 1, "amount": 5.00, "category": "X", "description": "y", "date": "2026-01-01 12:00"}]
        (tmp_path / "expenses.json").write_text(json.dumps(data))
        tracker = ExpenseTracker(data_file=str(tmp_path / "expenses.json"))
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0]["id"] == 1

    def test_missing_file_gives_empty_list(self, tmp_path):
        tracker = ExpenseTracker(data_file=str(tmp_path / "missing.json"))
        assert tracker.expenses == []


# ---------------------------------------------------------------------------
# prompt_add_expense
# ---------------------------------------------------------------------------

class TestPromptAddExpense:
    def test_valid_input_adds_expense(self, tracker):
        with patch("builtins.input", side_effect=["15.00", "Food", "Dinner"]):
            prompt_add_expense(tracker)
        assert len(tracker.expenses) == 1
        assert tracker.expenses[0]["amount"] == 15.00

    def test_invalid_amount_aborts(self, tracker, capsys):
        with patch("builtins.input", side_effect=["abc"]):
            prompt_add_expense(tracker)
        assert tracker.expenses == []
        assert "Invalid amount" in capsys.readouterr().out

    def test_zero_amount_aborts(self, tracker, capsys):
        with patch("builtins.input", side_effect=["0"]):
            prompt_add_expense(tracker)
        assert tracker.expenses == []
        assert "greater than zero" in capsys.readouterr().out

    def test_negative_amount_aborts(self, tracker, capsys):
        with patch("builtins.input", side_effect=["-5"]):
            prompt_add_expense(tracker)
        assert tracker.expenses == []

    def test_empty_category_aborts(self, tracker, capsys):
        with patch("builtins.input", side_effect=["10.00", "  "]):
            prompt_add_expense(tracker)
        assert tracker.expenses == []
        assert "Category cannot be empty" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# display_all_expenses
# ---------------------------------------------------------------------------

class TestDisplayAllExpenses:
    def test_empty_message(self, tracker, capsys):
        display_all_expenses(tracker)
        assert "No expenses recorded yet" in capsys.readouterr().out

    def test_shows_expense_row(self, populated_tracker, capsys):
        display_all_expenses(populated_tracker)
        out = capsys.readouterr().out
        assert "Food" in out
        assert "Transport" in out


# ---------------------------------------------------------------------------
# display_by_category
# ---------------------------------------------------------------------------

class TestDisplayByCategory:
    def test_empty_message(self, tracker, capsys):
        display_by_category(tracker)
        assert "No expenses recorded yet" in capsys.readouterr().out

    def test_shows_category_totals(self, populated_tracker, capsys):
        display_by_category(populated_tracker)
        out = capsys.readouterr().out
        assert "Food" in out
        assert "15.50" in out


# ---------------------------------------------------------------------------
# display_summary
# ---------------------------------------------------------------------------

class TestDisplaySummary:
    def test_empty_message(self, tracker, capsys):
        display_summary(tracker)
        assert "No expenses recorded yet" in capsys.readouterr().out

    def test_shows_total(self, populated_tracker, capsys):
        display_summary(populated_tracker)
        out = capsys.readouterr().out
        assert "35.50" in out
        assert "3" in out


# ---------------------------------------------------------------------------
# prompt_delete_expense
# ---------------------------------------------------------------------------

class TestPromptDeleteExpense:
    def test_delete_existing(self, populated_tracker, capsys):
        with patch("builtins.input", return_value="1"):
            prompt_delete_expense(populated_tracker)
        assert all(e["id"] != 1 for e in populated_tracker.expenses)
        assert "deleted" in capsys.readouterr().out

    def test_cancel_with_zero(self, populated_tracker):
        with patch("builtins.input", return_value="0"):
            prompt_delete_expense(populated_tracker)
        assert len(populated_tracker.expenses) == 3

    def test_missing_id_message(self, populated_tracker, capsys):
        with patch("builtins.input", return_value="999"):
            prompt_delete_expense(populated_tracker)
        assert "No expense found" in capsys.readouterr().out
        assert len(populated_tracker.expenses) == 3

    def test_invalid_id_message(self, populated_tracker, capsys):
        with patch("builtins.input", return_value="abc"):
            prompt_delete_expense(populated_tracker)
        assert "Invalid ID" in capsys.readouterr().out

    def test_empty_tracker_message(self, tracker, capsys):
        prompt_delete_expense(tracker)
        assert "No expenses to delete" in capsys.readouterr().out
