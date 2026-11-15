# Personal Finance Manager

A Python application for recording, editing and analyzing personal
financial transactions (income, expenses and adjustments), with both a
Console interface and a FreeSimpleGUI graphical interface sharing one
backend and the same CSV data files.

## 1. Installation

```bash
cd "Gestor de Finanzas Personales"
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` installs:

- `FreeSimpleGUI` — the GUI toolkit used by `ui/gui_ui.py`.
- `pytest` — used to run the unit tests in `tests/`.

## 2. Running the application

```bash
python3 main.py
```

You will see:

```
========================================
       PERSONAL FINANCE MANAGER
========================================

Select the application interface:

1. Console Mode (Text-Based)
2. GUI Mode (FreeSimpleGUI)
0. Exit
```

Choose `1` for the text-based menus or `2` to open the FreeSimpleGUI
window. Both modes read and write the same files in `data/`.

## 3. Running the tests

```bash
python3 -m pytest tests/ -v
```

Tests run against a disposable temporary copy of the CSV data (see
`tests/conftest.py`), so they never modify the real files in `data/`.

## 4. Project structure

```text
Gestor de Finanzas Personales/
├── main.py                 # Entry point: startup menu (Console / GUI / Exit)
├── core/
│   ├── category.py          # Category entity
│   ├── transaction.py       # Transaction entity
│   ├── validators.py        # Centralized validation rules
│   ├── exceptions.py        # Custom exception hierarchy
│   └── finance_manager.py   # Shared business logic (the backend)
├── storage/
│   └── file_manager.py      # All CSV reading/writing happens here
├── ui/
│   ├── console_ui.py        # Text-based front-end
│   └── gui_ui.py             # FreeSimpleGUI front-end
├── data/
│   ├── categories.csv
│   ├── types.csv
│   └── transactions.csv
├── tests/
│   ├── conftest.py
│   ├── test_categories.py
│   ├── test_transactions.py
│   └── test_validators.py
└── requirements.txt
```

## 5. Architecture

The application is split into three layers, and data flows strictly in one
direction: **UI → FinanceManager → FileManager → CSV files.**

1. **Presentation (`ui/console_ui.py`, `ui/gui_ui.py`)** — Only displays
   menus/windows, collects input, and shows success/error messages. Neither
   file opens a CSV file or contains a business rule; both call the exact
   same `FinanceManager` methods (e.g. `add_transaction`, `edit_category`).
2. **Business logic (`core/finance_manager.py`)** — The single source of
   truth for categories, transactions, validation and dashboard
   calculations. It uses `core/validators.py` for input validation and
   raises exceptions from `core/exceptions.py` when a rule is broken; it
   never prints or opens a window.
3. **Persistence (`storage/file_manager.py`)** — The only module that reads
   or writes `categories.csv`, `types.csv` and `transactions.csv`. Writes
   are "safe": each save writes to a temporary file first and then
   atomically replaces the target file, so an interrupted write cannot
   corrupt existing data.

Because both `ConsoleUI` and `GUIUI` are constructed with the *same*
`FinanceManager` instance in `main.py`, any action taken in one interface
(e.g. adding a category) is immediately reflected if you reopen the other.

### How this demonstrates the course's educational objectives

| Objective | Where it shows up |
|---|---|
| Modularization | `core/`, `storage/`, `ui/` each own a single responsibility |
| File handling | `storage/file_manager.py` centralizes all CSV I/O with safe temp-file writes |
| Input validation | `core/validators.py`'s `Validator` class |
| Functions & reuse | `Validator` and `FinanceManager` methods are called identically from both UIs |
| OOP | `Category`, `Transaction`, `FinanceManager`, `FileManager`, `Validator`, `ConsoleUI`, `GUIUI` classes |
| Separation of concerns | UI never touches CSVs; business logic never prints/draws windows |
| Data relationships | `transactions.csv` references `categories.csv` and `types.csv` by ID; deleting a referenced category is blocked |
| Exception handling | `core/exceptions.py` hierarchy, caught and displayed independently by each UI |
| Code reusability | Both UIs call the exact same `FinanceManager` API |

## 6. Business rules enforced by the backend

- Category names must be non-empty and unique (case-insensitive).
- A category cannot be deleted while it is referenced by a transaction.
- Income amounts are always stored as positive; Expense amounts are always
  stored as negative; Adjustment amounts may be positive or negative but
  never zero.
- Transaction IDs are unique, randomly generated 8-digit numbers.
- Editing a transaction preserves its original ID and creation timestamp.
- Amounts are handled with `Decimal` (not `float`) to avoid rounding errors,
  and are always stored with two decimal places.
