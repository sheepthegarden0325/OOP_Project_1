from datetime import datetime
from transaction import Transaction
from decimal import Decimal


class Account:
    def __init__(self, client, account_number: str):
        self.number = account_number
        self.client = client
        self.transactions = {  # this dictionary is for tracking transactions
            # "transaction_id": transaction_instance
        }
        self.current_balance = Decimal('0.0')

    def check_balance(self) -> Decimal:
        return self.current_balance

    def print_balance(self):
        print(
            f'Date & Time: {datetime.now()}, Account: {self.number}, Current balance: {self.current_balance}')
        return

    def add_balance(self, added_amount):
        self.current_balance += added_amount

    def remove_balance(self, removed_amount):
        self.current_balance -= removed_amount

    # Automatic transaction_id producing function
    def create_transaction_id(self):
        # transaction_id = date_time + ' ' + account_number: str
        return f'{datetime.now()} ' + self.number

    def deposit(self, bank, amount: Decimal, description='') -> bool:
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

    def withdraw(self, bank, amount: Decimal, description='') -> bool:
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

    def transfer(self, bank, remittee, amount: Decimal, description='') -> bool:
        # Transaction creation start
        transaction_id = self.create_transaction_id()
        transaction = Transaction(transaction_id,
                                  'Transfer',
                                  amount,
                                  description)
        transaction.remitter_account = self
        transaction.remittee_account = remittee
        # Transaction creation end

        # Auditing start
        bank.transactions[transaction_id] = transaction
        self.transactions[transaction_id] = transaction
        # Auditing end

        if amount <= Decimal('0.0'):  # Amount validation
            transaction.status_change_to_cancelled(3)  # Pending -> Cancelled
            return False

        # Checking if matching receiver account does not exist.
        if remittee is None:
            transaction.status_change_to_cancelled(1)  # Pending -> Cancelled
            return False
        if self.current_balance >= amount:  # checking balance
            receiver_balance = remittee.current_balance
            remittee.receive(amount, transaction)
            if remittee.current_balance != receiver_balance + amount:
                # Reinstate remittee's balance
                remittee.current_balance = receiver_balance
                transaction.status_change_to_cancelled(2)
                # Pending -> Cancelled
                return False
            self.remove_balance(amount)
            transaction.status_change_to_processed()  # Pending -> Processed
            transaction.print_transaction_result(self.current_balance, self)
            transaction.print_transaction_result(remittee.current_balance,
                                                 remittee)
            # Pending -> Processed
            return True
        else:
            transaction.status_change_to_cancelled(0)  # Panding -> Cancelled
            return False

    def receive(self, amount: Decimal, transaction: Transaction):
        self.add_balance(amount)
        self.transactions[transaction.id] = transaction
