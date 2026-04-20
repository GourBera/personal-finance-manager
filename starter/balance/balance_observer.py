# balance_observer.py


class IBalanceObserver:
    def update(self, balance, transaction):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class PrintObserver(IBalanceObserver):
    def update(self, balance, transaction):
        """Print balance update message."""
        print(f"[Balance Update] {transaction} → Current Balance: ${balance:.2f}")


class LowBalanceAlertObserver(IBalanceObserver):
    def __init__(self, threshold):
        self.threshold = threshold
        self.alert_triggered = False

    def update(self, balance, transaction):
        """Alert if balance drops below threshold."""
        if balance < self.threshold:
            self.alert_triggered = True
            print(f"LOW BALANCE ALERT: Balance ${balance:.2f} is below threshold ${self.threshold:.2f}!")
        else:
            self.alert_triggered = False
