# Expense Tracker — API Reference

All public classes and functions in `expense_tracker.py`. Data is persisted to a JSON file (`expenses.json` by default) in the working directory.

---

## Constants

| Name | Value | Description |
|------|-------|-------------|
| `DATA_FILE` | `"expenses.json"` | Default path for the persisted expense store |
| `DATE_FORMAT` | `"%Y-%m-%d %H:%M"` | Timestamp format used when recording expenses |
| `ALL_EXPENSES_TABLE_WIDTH` | `65` | Column width of the full-expense table separator |
| `CATEGORY_TABLE_WIDTH` | `32` | Column width of the category-totals table separator |

---

## Data Model

Each expense is a `dict` stored as an element in the JSON array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Auto-incremented unique identifier |
| `amount` | `float` | Rounded to 2 decimal places |
| `category` | `str` | User-supplied category label (e.g. `"Food"`) |
| `description` | `str` | Free-text description |
| `date` | `str` | Timestamp formatted with `DATE_FORMAT` |

---

## Class: `ExpenseTracker`

Manages a collection of expenses with file-backed persistence.

```python
tracker = ExpenseTracker(data_file="expenses.json")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data_file` | `str` | `DATA_FILE` | Path to the JSON file used for persistence |

### `ExpenseTracker.add(amount, category, description) -> dict`

Add a new expense and save to disk.

| Parameter | Type | Description |
|-----------|------|-------------|
| `amount` | `float` | Expense amount; caller is responsible for ensuring `> 0` |
| `category` | `str` | Category label |
| `description` | `str` | Free-text description |

**Returns:** The newly created expense `dict`.

**Side effects:** Appends to `self.expenses`; calls `_save()`.

---

### `ExpenseTracker.delete(expense_id) -> bool`

Remove an expense by ID.

| Parameter | Type | Description |
|-----------|------|-------------|
| `expense_id` | `int` | ID of the expense to remove |

**Returns:** `True` if the expense was found and deleted; `False` otherwise.

**Side effects:** Mutates `self.expenses` in-place; calls `_save()` on success.

---

### `ExpenseTracker.totals_by_category() -> dict[str, float]`

Return a mapping of category → total amount across all expenses.

**Returns:** `dict[str, float]` — keys are category strings, values are summed amounts.

No side effects.

---

### `ExpenseTracker.summary() -> dict | None`

Return aggregate statistics for all expenses.

**Returns:**

| Key | Type | Description |
|-----|------|-------------|
| `total` | `float` | Sum of all expense amounts |
| `count` | `int` | Number of expense entries |
| `average` | `float` | Mean amount per entry |

Returns `None` if there are no expenses.

No side effects.

---

### Private methods

| Method | Description |
|--------|-------------|
| `_load() -> list[dict]` | Read expenses from disk; returns `[]` if the file is absent. Raises `json.JSONDecodeError` on malformed JSON. |
| `_save() -> None` | Write `self.expenses` to disk (pretty-printed, 2-space indent), replacing previous content. |
| `_next_id() -> int` | Return `max(existing ids, default=0) + 1`. IDs remain unique after deletions. |

---

## UI Functions

These functions handle all `input()` / `print()` interaction. They accept an `ExpenseTracker` instance and return `None`.

### `prompt_add_expense(tracker) -> None`

Interactively collect a new expense from stdin.

**Prompts (in order):**
1. `Amount` — must parse as `float` and be `> 0`.
2. `Category` — must be non-empty after `.strip()`.
3. `Description` — optional free text.

Calls `tracker.add()` on valid input; prints an error and returns early on invalid input.

---

### `display_all_expenses(tracker) -> None`

Print a formatted table of all expenses to stdout.

Columns: `ID`, `Date`, `Category`, `Amount`, `Description`.

Prints `"No expenses recorded yet."` if the list is empty.

---

### `display_by_category(tracker) -> None`

Print per-category totals sorted alphabetically.

Prints `"No expenses recorded yet."` if the list is empty.

---

### `display_summary(tracker) -> None`

Print total spending, entry count, and average amount per entry.

Prints `"No expenses recorded yet."` if the list is empty.

---

### `prompt_delete_expense(tracker) -> None`

Display all expenses, then prompt the user for an ID to delete.

- Enter `0` to cancel without deleting.
- Prints an error message if the ID is not found.

---

## Entry Point

### `main() -> None`

Load expenses from disk via `ExpenseTracker`, then run an interactive menu loop until the user selects **Quit**.

| Key | Action |
|-----|--------|
| `1` | `prompt_add_expense` |
| `2` | `display_all_expenses` |
| `3` | `display_by_category` |
| `4` | `display_summary` |
| `5` | `prompt_delete_expense` |
| `6` | Quit |

---

## Data File

**Default path:** `./expenses.json` (relative to the working directory at runtime)

**Format:**
```json
[
  {
    "id": 1,
    "amount": 12.50,
    "category": "Food",
    "description": "Lunch",
    "date": "2026-05-16 13:45"
  }
]
```

The file is always written in full on every mutation — there is no partial update.
