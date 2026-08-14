from datetime import datetime
from transaction import Transaction
from client import Client


class Account:
    def __init__(self, client: Client, account_number: str):
        self.number = account_number
        self.clinet = client
        self.transaction_records = {  # this dictionary is for tracking transactions
            # "transaction_id": transaction_instance

        }
        self.current_balance = 0.0

    def add_balance(self, added_amount):
        self.current_balance += added_amount

    def remove_balace(self, removed_amount):
        self.current_balance -= removed_amount

    def deposit(self, amount: float, description: str) -> bool:
        transaction_id = f'{datetime.now()} ' + self.number
        transaction = Transaction(
            transaction_id, 'deposit', amount, description)
        self.transaction_records[transaction_id] = transaction
        self.add_balance(amount)
        transaction.status_change_to_processed(self.current_balance)
        return True

    def withdraw(self, amount: float, description: str) -> bool:
        transaction_id = f'{datetime.now()} ' + self.number
        transaction = Transaction(
            transaction_id, 'withdrawal', amount, description)
        if self.current_balance >= amount:  # checking balance
            self.remove_balace(amount)
            transaction.status_change_to_processed(
                self.current_balance)  # Pending -> Processed
            return True
        else:
            transaction.status_change_to_cancelled(
                self.current_balance)  # Pending -> Cancelled

            return False

    def transfer(self, transfer_to_this_account: str, amount: float, description: str) -> bool:
        transaction_id = f'{datetime.now()} ' + self.number
        transaction = Transaction(transaction_id,
                                  'withdrawal',
                                  amount,
                                  description)
        if self.current_balance >= amount:  # checking balance
            self.remove_balace(amount)
            self.transaction_records.append({"date_time": datetime.now(),
                                             "transaction_type": "transfer",
                                             "transfer_to_this_account": transfer_to_this_account,
                                             "amount": amount})
            print(f"Date & Time: {datetime.now()} Transaction succeeded, Transaction type: transfer, Remittee: {transfer_to_this_account}, Amount: ${amount}, Current balance: {self.current_balance}")
            return True
        else:
            print("Transaction failed: not enough balance")
            return False

    def receive(self, received_from_this_account: str, received_amount: float) -> bool:
        self.add_balance(received_amount)
        self.transaction_records.append({"date_time": datetime.now(),
                                         "transaction_type": "transfer",
                                         "received_from_this_account": received_from_this_account,
                                         "amount": received_amount})
        print(f"Date & Time: {datetime.now()} Transaction succeeded, Transaction type: transfer, Remitter: {received_from_this_account}, Amount: ${received_amount}, Current balance: {self.current_balance}")
        return True
