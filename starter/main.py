"""This module serves as the entry point for the program."""
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver
from balance.balance_observer import PrintBalanceObserver
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_adapter import TransactionAdapter
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_command import ApplyTransactionCommand, TransactionHistory


def main():
    print("=" * 50)
    print("Personal Finance Manager")
    print("=" * 50)

    # Create balance singleton and register observers
    balance = Balance.get_instance()
    balance.register_observer(PrintBalanceObserver())
    balance.register_observer(LowBalanceAlertObserver(threshold=100))

    # Create standard transactions
    transactions = [
        Transaction(100, TransactionCategory.INCOME),
        Transaction(50, TransactionCategory.EXPENSE),
        Transaction(200, TransactionCategory.INCOME),
        Transaction(75, TransactionCategory.EXPENSE),
    ]

    # Create an external income transaction (via Adapter pattern)
    freelance_income = ExternalFreelanceIncome(1200, "INV-98765", "Mobile App Project")
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()

    all_transactions = transactions + [adapted_transaction]

    # Apply all transactions using the Command pattern for undo/redo support
    history = TransactionHistory()
    print("\nProcessing transactions...")
    print("-" * 50)
    for t in all_transactions:
        cmd = ApplyTransactionCommand(balance, t)
        history.execute(cmd)

    print("-" * 50)
    print(f"\n{balance.summary()}")

    print("\nBalance before undo/redo:")
    print(balance.summary())

    # Demonstrate undo/redo capability (Command pattern)
    print("\n" + "=" * 50)
    print("Demonstrating Undo/Redo (Command Pattern)")
    print("=" * 50)

    print("\nUndoing last transaction...")
    history.undo()
    print(f"{balance.summary()}")

    print("\nUndoing another transaction...")
    history.undo()
    print(f"{balance.summary()}")

    print("\nRedoing last undone transaction...")
    history.redo()
    print(f"{balance.summary()}")


if __name__ == "__main__":
    main()
