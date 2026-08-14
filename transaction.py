from datetime import datetime
from decimal import Decimal


class Transaction:

    def __init__(self, id, type, amount: Decimal, description):
        self.id = id
        self.date_time = datetime.now()
        self.type = type
        self.amount = amount
        self.description = description
        self.remitter_account = None
        self.remittee_account = None
        self.status = 'Pending'

    def status_change_to_processed(self):
        if self.status == 'Pending':
            self.status = 'Processed'
            self.date_time = datetime.now()  # Time updates
            return True

        else:
            return False

    def status_change_to_cancelled(self, error_code: int):

        if self.status == "Pending":
            self.status = "Cancelled"
            self.date_time = datetime.now()  # Time updates
            if error_code == 0:  # error_code: 0 -> Not enough balance
                print(
                    f"Date & Time: {datetime.now()}, Transaction failed: Not enough balance.")
            elif error_code == 1:  # error_code: 1 -> No matching receiver account
                print(
                    f"Date & Time: {datetime.now()}, Transaction failed: No matching remittee account.")
            elif error_code == 2:  # error_code: 2 -> System failed adding exact amount of money on receiver account
                print(
                    f"Date & Time: {datetime.now()}, Transaction failed: Banking system calculation error.")
            elif error_code == 3:  # error_code: 3 -> Wrong amount input
                print(
                    f"Date & Time: {datetime.now()}, Transaction failed: Amount cannot be 0 or negative.")
            return True

        else:
            return False

    def print_transaction_result(self, current_balance, viewer_account=None):
        if self.type == 'Deposit':
            print(
                f"Date & Time: {datetime.now()}, Transaction succeeded, Transaction type: Deposit, Amount: + ${self.amount}, Current balance: {current_balance}")
        elif self.type == 'Withdrawal':
            print(
                f"Date & Time: {datetime.now()}, Transaction succeeded, Transaction type: Withdrawal, Amount: - ${self.amount}, Current balance: {current_balance}")
        elif self.type == 'Transfer':
            if viewer_account is self.remittee_account:  # Message for remittee
                print(
                    f"Date & Time: {datetime.now()} Transaction succeeded, Transaction type: Transfer, Remitter: {self.remitter_account.number}, Amount: + ${self.amount}, Current balance: {current_balance}")
            elif viewer_account is self.remitter_account:  # message for remitter
                print(
                    f"Date & Time: {datetime.now()}, Transaction succeeded, Transaction type: Transfer, Remittee: {self.remittee_account.number}, Amount: - ${self.amount}, Current balance: {current_balance}")

    def update_transaction_description(self, description: str):
        self.description = description
