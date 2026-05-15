# Expense Tracker — API Reference

All public functions in `expense_tracker.py`. The data store is a JSON file (`expenses.json`) in the working directory.

---

## Data Model

Each expense is a dict stored in the JSON array:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Auto-incremented unique identifier |
| `amount` | `float` | Rounded to 2 decimal places |
| `category` | `str` | User-supplied category label (e.g. `"Food"`) |
| `description` | `str` | Free-text description |
| `date` | `str` | Timestamp in `"YYYY-MM-DD HH:MM"` format |

---

## Functions

### `load_expenses() -> list[dict]`

Reads all expenses from `expenses.json`.

- Returns an empty list if the file does not exist.
- Raises `json.JSONDecodeError` if the file is malformed.

---

### `save_expenses(expenses: list[dict]) -> None`

Writes the full expenses list to `expenses.json` (pretty-printed, 2-space indent), overwriting any previous content.

| Parameter | Type | Description |
|-----------|------|-------------|
| `expenses` | `list[dict]` | The complete list of expense dicts to persist |

---

### `add_expense(expenses: list[dict]) -> None`

Interactive prompt that collects a new expense from stdin and appends it to `expenses`, then calls `save_expenses`.

**Prompts:**
1. `Amount` — must parse as `float`; rejects non-numeric input.
2. `Category` — must be non-empty after `.strip()`.
3. `Description` — optional free text.

**ID assignment:** `max(existing ids, default=0) + 1`

**Side effects:** Mutates `expenses` in-place; calls `save_expenses`.

---

### `view_expenses(expenses: list[dict]) -> None`

Prints a formatted table of all expenses to stdout.

Columns: `ID`, `Date`, `Category`, `Amount`, `Description`.

No return value; no side effects on data.

---

### `view_by_category(expenses: list[dict]) -> None`

Aggregates and prints total spending per category, sorted alphabetically.

No return value; no side effects on data.

---

### `calculate_total(expenses: list[dict]) -> None`

Prints summary statistics to stdout:
- Total spending
- Number of entries
- Average amount per entry

No return value; no side effects on data.

---

### `delete_expense(expenses: list[dict]) -> None`

Interactive prompt that displays all expenses, then removes the entry matching the user-supplied ID.

- Enter `0` to cancel without deleting.
- Prints an error if the ID is not found.

**Side effects:** Mutates `expenses` in-place; calls `save_expenses` on successful deletion.

---

### `main() -> None`

Entry point. Loads expenses from disk, then runs an interactive menu loop until the user selects **Quit**.

Menu options:

| Key | Action |
|-----|--------|
| `1` | `add_expense` |
| `2` | `view_expenses` |
| `3` | `view_by_category` |
| `4` | `calculate_total` |
| `5` | `delete_expense` |
| `6` | Quit |

---

## Data File

**Path:** `./expenses.json` (relative to the working directory at runtime)

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