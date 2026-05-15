import json
from collections import defaultdict
from datetime import datetime


DATA_FILE = "expenses.json"


def load_expenses():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses):
    print("\n--- Add New Expense ---")
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    category = input("Category (e.g. Food, Transport, Utilities): ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    description = input("Description: ").strip()

    expense = {
        "id": max((e["id"] for e in expenses), default=0) + 1,
        "amount": round(amount, 2),
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense of ${amount:.2f} added successfully.")


def view_expenses(expenses):
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"{'ID':<5} {'Date':<17} {'Category':<15} {'Amount':>8}  Description")
    print("-" * 65)
    for e in expenses:
        print(
            f"{e['id']:<5} {e['date']:<17} {e['category']:<15} ${e['amount']:>7.2f}  {e['description']}"
        )


def view_by_category(expenses):
    print("\n--- Expenses by Category ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]

    print(f"{'Category':<20} {'Total':>10}")
    print("-" * 32)
    for category, total in sorted(totals.items()):
        print(f"{category:<20} ${total:>9.2f}")


def calculate_total(expenses):
    print("\n--- Total Spending ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    total = sum(e["amount"] for e in expenses)
    print(f"Total expenses: ${total:.2f}")
    print(f"Number of entries: {len(expenses)}")
    print(f"Average per entry: ${total / len(expenses):.2f}")


def delete_expense(expenses):
    print("\n--- Delete Expense ---")
    if not expenses:
        print("No expenses to delete.")
        return

    view_expenses(expenses)
    try:
        expense_id = int(input("\nEnter ID to delete (0 to cancel): "))
    except ValueError:
        print("Invalid ID.")
        return

    if expense_id == 0:
        return

    for i, e in enumerate(expenses):
        if e["id"] == expense_id:
            expenses.pop(i)
            break
    else:
        print(f"No expense found with ID {expense_id}.")
        return
    save_expenses(expenses)
    print(f"Expense #{expense_id} deleted.")


def main():
    expenses = load_expenses()

    menu = {
        "1": ("Add expense", lambda: add_expense(expenses)),
        "2": ("View all expenses", lambda: view_expenses(expenses)),
        "3": ("View by category", lambda: view_by_category(expenses)),
        "4": ("Calculate total spending", lambda: calculate_total(expenses)),
        "5": ("Delete an expense", lambda: delete_expense(expenses)),
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
