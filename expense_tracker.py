import json
from collections import defaultdict
from datetime import datetime
from typing import Optional


DATA_FILE = "expenses.json"
DATE_FORMAT = "%Y-%m-%d %H:%M"
ALL_EXPENSES_TABLE_WIDTH = 65
CATEGORY_TABLE_WIDTH = 32


class ExpenseTracker:
    """Manages a collection of expenses with file-backed persistence."""

    def __init__(self, data_file: str = DATA_FILE) -> None:
        self.data_file = data_file
        self.expenses: list[dict] = self._load()

    def _load(self) -> list[dict]:
        """Load expenses from disk, returning an empty list if the file is absent."""
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save(self) -> None:
        """Persist the current expenses list to disk."""
        with open(self.data_file, "w") as f:
            json.dump(self.expenses, f, indent=2)

    def _next_id(self) -> int:
        """Return the next available expense ID."""
        return max((e["id"] for e in self.expenses), default=0) + 1

    def add(self, amount: float, category: str, description: str) -> dict:
        """Add a new expense and save to disk."""
        expense = {
            "id": self._next_id(),
            "amount": round(amount, 2),
            "category": category,
            "description": description,
            "date": datetime.now().strftime(DATE_FORMAT),
        }
        self.expenses.append(expense)
        self._save()
        return expense

    def delete(self, expense_id: int) -> bool:
        """Remove an expense by ID. Returns True if found and deleted."""
        for i, e in enumerate(self.expenses):
            if e["id"] == expense_id:
                self.expenses.pop(i)
                self._save()
                return True
        return False

    def totals_by_category(self) -> dict[str, float]:
        """Return a mapping of category -> total amount."""
        totals: dict[str, float] = defaultdict(float)
        for e in self.expenses:
            totals[e["category"]] += e["amount"]
        return dict(totals)

    def summary(self) -> Optional[dict]:
        """Return total, count, and average, or None if there are no expenses."""
        if not self.expenses:
            return None
        total = sum(e["amount"] for e in self.expenses)
        return {
            "total": total,
            "count": len(self.expenses),
            "average": total / len(self.expenses),
        }


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------

def prompt_add_expense(tracker: ExpenseTracker) -> None:
    """Interactively prompt the user for a new expense and add it."""
    print("\n--- Add New Expense ---")
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    category = input("Category (e.g. Food, Transport, Utilities): ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    description = input("Description: ").strip()
    expense = tracker.add(amount, category, description)
    print(f"Expense of ${expense['amount']:.2f} added successfully.")


def display_all_expenses(tracker: ExpenseTracker) -> None:
    """Print a formatted table of all expenses."""
    print("\n--- All Expenses ---")
    if not tracker.expenses:
        print("No expenses recorded yet.")
        return

    print(f"{'ID':<5} {'Date':<17} {'Category':<15} {'Amount':>8}  Description")
    print("-" * ALL_EXPENSES_TABLE_WIDTH)
    for e in tracker.expenses:
        print(
            f"{e['id']:<5} {e['date']:<17} {e['category']:<15} ${e['amount']:>7.2f}  {e['description']}"
        )


def display_by_category(tracker: ExpenseTracker) -> None:
    """Print per-category totals."""
    print("\n--- Expenses by Category ---")
    if not tracker.expenses:
        print("No expenses recorded yet.")
        return

    totals = tracker.totals_by_category()
    print(f"{'Category':<20} {'Total':>10}")
    print("-" * CATEGORY_TABLE_WIDTH)
    for category, total in sorted(totals.items()):
        print(f"{category:<20} ${total:>9.2f}")


def display_summary(tracker: ExpenseTracker) -> None:
    """Print total, count, and average spending."""
    print("\n--- Total Spending ---")
    stats = tracker.summary()
    if stats is None:
        print("No expenses recorded yet.")
        return

    print(f"Total expenses:    ${stats['total']:.2f}")
    print(f"Number of entries: {stats['count']}")
    print(f"Average per entry: ${stats['average']:.2f}")


def prompt_delete_expense(tracker: ExpenseTracker) -> None:
    """Interactively prompt the user to select and delete an expense."""
    print("\n--- Delete Expense ---")
    if not tracker.expenses:
        print("No expenses to delete.")
        return

    display_all_expenses(tracker)
    try:
        expense_id = int(input("\nEnter ID to delete (0 to cancel): "))
    except ValueError:
        print("Invalid ID.")
        return

    if expense_id == 0:
        return

    if tracker.delete(expense_id):
        print(f"Expense #{expense_id} deleted.")
    else:
        print(f"No expense found with ID {expense_id}.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the interactive expense tracker menu loop."""
    tracker = ExpenseTracker()

    menu = {
        "1": ("Add expense", lambda: prompt_add_expense(tracker)),
        "2": ("View all expenses", lambda: display_all_expenses(tracker)),
        "3": ("View by category", lambda: display_by_category(tracker)),
        "4": ("Calculate total spending", lambda: display_summary(tracker)),
        "5": ("Delete an expense", lambda: prompt_delete_expense(tracker)),
        "6": ("Quit", None),
    }

    print("=== Expense Tracker ===")
    while True:
        print("\nMenu:")
        for key, (label, _) in menu.items():
            print(f"  {key}. {label}")

        choice = input("\nChoose an option: ").strip()

        if choice not in menu:
            print("Invalid option. Please try again.")
        elif menu[choice][1] is None:
            print("Goodbye!")
            break
        else:
            menu[choice][1]()


if __name__ == "__main__":
    main()
