# Personal Finance Manager — Design Pattern Reflection

## Overview

This application is a simple personal finance manager that tracks income and expenses, monitors balance, and alerts users when the balance falls below a threshold. Four design patterns were used to achieve a modular, testable, and extensible architecture.

---

## 1. Singleton Pattern — `Balance`

**Where it's used:** The `Balance` class in `balance/balance.py` uses the Singleton pattern to ensure only one instance of the balance manager exists throughout the application.

**Why it was chosen:** In a financial application, having multiple balance instances could lead to inconsistent state — one part of the code might show a different balance than another. The Singleton guarantees a single source of truth for the user's net balance across all modules.

**How it improves the design:** Any module that needs to read or modify the balance calls `Balance.get_instance()` and is guaranteed to work with the same data. This eliminates synchronization bugs and simplifies the mental model of the application.

**Trade-offs:** Singleton introduces global state, which can make unit testing harder — tests must call `reset()` in `setUp` to avoid state leaking between tests. It also makes the class harder to replace or mock in isolation tests, though the `reset()` method mitigates this.

---

## 2. Adapter Pattern — `TransactionAdapter`

**Where it's used:** The `TransactionAdapter` class in `transaction/transaction_adapter.py` converts `ExternalFreelanceIncome` objects (from a third-party freelance platform) into the application's internal `Transaction` format.

**Why it was chosen:** External income data arrives with a different structure (invoice ID, project description, and a string type field) that doesn't match our internal `Transaction(amount, TransactionCategory)` format. Rather than modifying either the external class or our core Transaction class, the Adapter bridges the gap.

**How it improves the design:** The core application code never needs to know about external data formats. If a new external source is added (e.g., a bank API), we simply create a new adapter — no changes to `Balance`, `Transaction`, or any existing code. This follows the Open/Closed Principle.

**Trade-offs:** Each new external format requires its own adapter class, which adds a small amount of boilerplate. However, this is far preferable to polluting the core domain model with format-specific logic.

---

## 3. Observer Pattern — `LowBalanceAlertObserver` and `PrintObserver`

**Where it's used:** The `Balance` class acts as the subject, maintaining a list of observers. `LowBalanceAlertObserver` and `PrintObserver` in `balance/balance_observer.py` are concrete observers that react to balance changes.

**Why it was chosen:** The balance needs to trigger side effects (printing updates, alerting on low balance) whenever a transaction is applied, but it shouldn't be responsible for knowing what those side effects are. The Observer pattern decouples the "what changed" (balance update) from the "what to do about it" (print, alert, log, etc.).

**How it improves the design:** New behaviors can be added by simply creating a new observer class and registering it — no modifications to `Balance`. For example, adding email notifications or audit logging would require zero changes to existing code. The `LowBalanceAlertObserver` also dynamically resets its alert when the balance recovers, providing accurate real-time status.

**Trade-offs:** Observers are notified in registration order, and debugging notification chains can be difficult if many observers are registered. There's also a risk of observers holding references that prevent garbage collection, though this isn't a concern in our small application.

---

## 4. Command Pattern — `ApplyTransactionCommand` and `TransactionHistory` (Student's Choice)

**Where it's used:** The `ApplyTransactionCommand` class in `transaction/transaction_command.py` encapsulates transaction application as a command object. `TransactionHistory` manages a stack of executed commands and provides undo/redo operations.

**Why it was chosen:** Financial applications benefit greatly from the ability to reverse mistakes. The Command pattern was selected because it naturally supports undo/redo by encapsulating each action as an object with both `execute()` and `undo()` methods. This is listed as a standout feature in the project rubric ("Add Undo/Redo Capability with Command Pattern").

**How it improves the design:**
- **Undo/Redo:** Users can reverse the last transaction and re-apply it, which is critical for error correction in a finance app.
- **Decoupling:** The invoker (`TransactionHistory`) doesn't know the details of how a transaction is applied — it just calls `execute()` or `undo()` on command objects.
- **Extensibility:** New command types (e.g., `TransferCommand`, `BudgetAdjustmentCommand`) can be added without modifying `TransactionHistory`.
- **Testability:** Each command can be tested in isolation for both its forward and reverse behavior.

**Trade-offs:** The command history consumes memory proportional to the number of transactions (each command stores a reference to its transaction and balance). For a large number of transactions, a limit on history depth might be needed. The undo operation also triggers observer notifications (the reverse transaction is applied through `apply_transaction`), which is correct behavior but means observers see both the original and the reversal.

---

## Summary

| Pattern | Component | Key Benefit |
|---------|-----------|-------------|
| Singleton | `Balance` | Single source of truth for balance state |
| Adapter | `TransactionAdapter` | Integrates external data without modifying core classes |
| Observer | `LowBalanceAlertObserver`, `PrintObserver` | Decoupled, extensible event notifications |
| Command | `ApplyTransactionCommand`, `TransactionHistory` | Undo/redo support with encapsulated actions |

All four patterns work together to create a modular application where each component has a single responsibility and can be extended or tested independently.

## Getting Started

### Dependencies

python version >= 3.10.x 


### Installation

1. Clone the repo:

```
bash
git clone https://github.com/udacity/cd14600-project-starter.git
cd cd14600-project-starter/starter
```

2. Run the Program: 
```
python main.py
```

## Testing

This project uses Python’s built-in unittest framework.

To run all tests:

```
python -m unittest discover
```

To run a single test file:
```
python -m unittest balance/test_balance_observer.py
```

### Break Down Tests

- test_balance.py → Verifies correct implementation of the Singleton Balance class.
- test_transaction.py → Confirms transactions update balances correctly.
- test_transaction_adapter.py → Ensures external income data is correctly adapted into Transaction objects.
- test_balance_observer.py → Validates that low-balance alerts are triggered at the correct threshold.

## Project Instructions

1. Implement Singleton Balance Class – Ensure only one balance object exists throughout the app.
2. Complete Transaction Class – Handle income and expense transactions.
3. Implement Adapter Pattern – Adapt external freelance income data into internal Transaction objects.
4. Implement Observer Pattern – Create a low balance observer that triggers an alert when funds drop too low.
5. Add Unit Tests – Write tests for all implemented functionality.
6. Choose and Implement a Fourth Pattern – Pick one additional design pattern (e.g., Strategy, Command, Decorator, etc.) and integrate it into your project.
7. Provide a Reflection – Add a short write-up in your repo (README or separate file) explaining your design choices.

## Built With

* [Python](https://www.python.org/) – Main programming language
* [unittest](https://docs.python.org/3/library/unittest.html) – Testing framework
* [PEP8](https://peps.python.org/pep-0008/) – Style guide for Python code

