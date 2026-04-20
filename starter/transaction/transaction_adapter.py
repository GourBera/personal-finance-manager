# transaction_adapter.py

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class TransactionAdapter:
    def __init__(self, external_transaction):
        self.external_transaction = external_transaction

    def to_transaction(self):
        """Convert an external transaction to a standard Transaction."""
        required = ("amount", "invoice_id", "description")
        missing = [field for field in required if not hasattr(self.external_transaction, field)]
        if missing:
            raise ValueError(f"Missing fields: {', '.join(missing)}")
        return Transaction(self.external_transaction.amount, TransactionCategory.INCOME)
