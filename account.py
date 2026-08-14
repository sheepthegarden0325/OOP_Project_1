from datetime import datetime
from transaction import Transaction
from client import Client
from bank import Bank
from decimal import Decimal


class Account:
    def __init__(self, client: Client, account_number: str):
        self.number = account_number
        self.client = client
        self.transactions = {  # this dictionary is for tracking transactions
            # "transaction_id": transaction_instance

        }
        self.current_balance = Decimal('0.0')

    def add_balance(self, added_amount):
        self.current_balance += added_amount

    def remove_balance(self, removed_amount):
        self.current_balance -= removed_amount

    # Automatic transaction_id producing function
    def create_transaction_id(self):
        # transaction_id = date_time + ' ' + account_number: str
        return f'{datetime.now()} ' + self.number

    def deposit(self, amount: Decimal, description: str, bank: Bank) -> bool:
        # Transaction creation start
        transaction_id = self.create_transaction_id()
        transaction = Transaction(transaction_id,
                                  'Deposit',
                                  amount,
                                  description)
        # Transaction creation end

        # Auditing start
        bank.transactions[transaction_id] = transaction
        self.transactions[transaction_id] = transaction
        # Auditing end

        if amount <= Decimal('0.0'):  # Amount validation
            transaction.status_change_to_cancelled(3)  # Pending -> Cancelled
            return False

        self.add_balance(amount)
        transaction.status_change_to_processed()
        # Pending -> Processed
        transaction.print_transaction_result(self.current_balance)
        return True

    def withdraw(self, amount: Decimal, description: str, bank: Bank) -> bool:
        # Transaction cration start
        transaction_id = self.create_transaction_id()
        transaction = Transaction(transaction_id,
                                  'Withdrawal',
                                  amount,
                                  description)
        # Transaction creation end

        # Auditing start
        bank.transactions[transaction_id] = transaction
        self.transactions[transaction_id] = transaction
        # Auditing end

        if amount <= Decimal('0.0'):  # Amount validation
            transaction.status_change_to_cancelled(3)  # Pending -> Cancelled
            return False

        if self.current_balance >= amount:  # checking balance
            self.remove_balance(amount)
            transaction.status_change_to_processed()
            # Pending -> Processed
            transaction.print_transaction_result(self.current_balance)
            return True

        else:
            transaction.status_change_to_cancelled(0)
            # Pending -> Cancelled
            return False

    def transfer(self, remittee: str, amount: Decimal, description: str, bank: Bank) -> bool:
        # Transaction creation start
        transaction_id = self.create_transaction_id()
        transaction = Transaction(transaction_id,
                                  'Transfer',
                                  amount,
                                  description)
        transaction.remitter_account = self
        transaction.remittee_account = bank.accounts.get(remittee)
        # Transaction creation end

        # Auditing start
        bank.transactions[transaction_id] = transaction
        self.transactions[transaction_id] = transaction
        # Auditing end

        if amount <= Decimal('0.0'):  # Amount validation
            transaction.status_change_to_cancelled(3)  # Pending -> Cancelled
            return False

        # Checking if matching receiver account does not exist.
        if transaction.remittee_account is None:
            transaction.status_change_to_cancelled(1)  # Pending -> Cancelled
            return False
        if self.current_balance >= amount:  # checking balance
            receiver_balance = transaction.remittee_account.current_balance
            transaction.remittee_account.receive(amount, transaction)
            if transaction.remittee_account.current_balance != receiver_balance + amount:
                # Reinstate remittee's balance
                transaction.remittee_account.current_balance = receiver_balance
                transaction.status_change_to_cancelled(2)
                # Pending -> Cancelled
                return False
            self.remove_balance(amount)
            transaction.status_change_to_processed()  # Pending -> Processed
            transaction.print_transaction_result(self.current_balance, self)
            transaction.print_transaction_result(transaction.remittee_account.current_balance,
                                                 transaction.remittee_account)
            # Pending -> Processed
            return True
        else:
            transaction.status_change_to_cancelled(0)  # Panding -> Cancelled
            return False

    def receive(self, amount: Decimal, transaction: Transaction):
        self.add_balance(amount)
        self.transactions[transaction.id] = transaction
