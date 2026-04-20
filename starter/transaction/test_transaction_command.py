import unittest
from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_command import ApplyTransactionCommand, TransactionHistory


class TestApplyTransactionCommand(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_execute_applies_income(self):
        cmd = ApplyTransactionCommand(self.balance, Transaction(100, TransactionCategory.INCOME))
        cmd.execute()
        self.assertEqual(self.balance.get_balance(), 100)

    def test_execute_applies_expense(self):
        cmd = ApplyTransactionCommand(self.balance, Transaction(50, TransactionCategory.EXPENSE))
        cmd.execute()
        self.assertEqual(self.balance.get_balance(), -50)

    def test_undo_reverses_income(self):
        cmd = ApplyTransactionCommand(self.balance, Transaction(100, TransactionCategory.INCOME))
        cmd.execute()
        self.assertEqual(self.balance.get_balance(), 100)
        cmd.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_undo_reverses_expense(self):
        cmd = ApplyTransactionCommand(self.balance, Transaction(50, TransactionCategory.EXPENSE))
        cmd.execute()
        self.assertEqual(self.balance.get_balance(), -50)
        cmd.undo()
        self.assertEqual(self.balance.get_balance(), 0)


class TestTransactionHistory(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.history = TransactionHistory()

    def test_execute_and_undo(self):
        cmd = ApplyTransactionCommand(self.balance, Transaction(200, TransactionCategory.INCOME))
        self.history.execute(cmd)
        self.assertEqual(self.balance.get_balance(), 200)
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_undo_then_redo(self):
        cmd = ApplyTransactionCommand(self.balance, Transaction(150, TransactionCategory.INCOME))
        self.history.execute(cmd)
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 0)
        self.history.redo()
        self.assertEqual(self.balance.get_balance(), 150)

    def test_multiple_undo(self):
        cmd1 = ApplyTransactionCommand(self.balance, Transaction(100, TransactionCategory.INCOME))
        cmd2 = ApplyTransactionCommand(self.balance, Transaction(30, TransactionCategory.EXPENSE))
        self.history.execute(cmd1)
        self.history.execute(cmd2)
        self.assertEqual(self.balance.get_balance(), 70)
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 100)
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_redo_cleared_after_new_execute(self):
        cmd1 = ApplyTransactionCommand(self.balance, Transaction(100, TransactionCategory.INCOME))
        cmd2 = ApplyTransactionCommand(self.balance, Transaction(50, TransactionCategory.EXPENSE))
        self.history.execute(cmd1)
        self.history.undo()
        self.history.execute(cmd2)
        # Redo stack should be cleared; redo should do nothing
        self.history.redo()
        self.assertEqual(self.balance.get_balance(), -50)

    def test_undo_empty_history(self):
        # Should not raise, just prints message
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_redo_empty_stack(self):
        # Should not raise, just prints message
        self.history.redo()
        self.assertEqual(self.balance.get_balance(), 0)


if __name__ == "__main__":
    unittest.main()
