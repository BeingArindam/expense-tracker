# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
python expense_tracker.py
```

No dependencies beyond the Python 3 standard library — no install step needed.

## Architecture

The entire application lives in a single file, `expense_tracker.py`. It is structured as a set of standalone functions that each accept the in-memory `expenses` list and operate on it; `main()` owns the load/menu loop.

Data is persisted to `expenses.json` in the working directory. The list is loaded once at startup (`load_expenses`) and written back in full after every mutation (`save_expenses`). There is no partial update — every write replaces the file.

ID generation uses `max(existing ids, default=0) + 1`, so IDs remain unique after deletions (not just `len + 1`).

## Custom slash commands

`.claude/commands/expense-tracker-doc.md` defines `/expense-tracker-doc [--api|--readme]` for generating documentation from the codebase.