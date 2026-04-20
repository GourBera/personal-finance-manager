# transaction_command.py

from abc import ABC, abstractmethod
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class ICommand(ABC):
    """Abstract command interface for the Command pattern."""

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class ApplyTransactionCommand(ICommand):
    """Command that applies a transaction to the balance and supports undo."""

    def __init__(self, balance, transaction):
        self.balance = balance
        self.transaction = transaction

    def execute(self):
        """Apply the transaction to the balance."""
        self.balance.apply_transaction(self.transaction)

    def undo(self):
        """Reverse the transaction by applying the opposite operation."""
        if self.transaction.category == TransactionCategory.INCOME:
            reverse = Transaction(self.transaction.amount, TransactionCategory.EXPENSE)
        else:
            reverse = Transaction(self.transaction.amount, TransactionCategory.INCOME)
        self.balance.apply_transaction(reverse)


class TransactionHistory:
    """Manages executed commands and supports undo/redo operations."""

    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def execute(self, command):
        """Execute a command and push it onto the undo stack."""
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self):
        """Undo the last executed command."""
        if not self._undo_stack:
            print("Nothing to undo.")
            return
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self):
        """Redo the last undone command."""
        if not self._redo_stack:
            print("Nothing to redo.")
            return
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)
