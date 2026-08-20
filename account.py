from datetime import datetime
from transaction import Transaction
from decimal import Decimal
from bank import Bank


class Account:
    __next_number = 1

    def __init__(self, client):
        self.__number = Account.__next_number
        Account.__next_number += 1
        from client import Client
        if isinstance(client, Client):
            # when an account is created automatically add in the client's account dictionary
            client.add_account(self)
        self.__transactions = {  # this dictionary is for tracking transactions
            # "transaction_id": transaction_instance
        }
        self.__current_balance = Decimal('0.0')
        Bank.add_account(self)

    def get_number(self) -> int:
        return self.__number

    def get_balance(self) -> Decimal:
        return self.__current_balance

    def print_balance(self):
        print(
            f'Date & Time: {datetime.now()}',
            f'Account: {self.__number}',
            f'Current balance: {self.__current_balance}',
            sep=', '
        )
        return

    def __add_balance(self, added_amount):
        self.__current_balance += added_amount

    def __remove_balance(self, removed_amount):
        self.__current_balance -= removed_amount

    def __create_transaction(self, type, amount, description) -> Transaction:
        transaction = Transaction(type,
                                  amount,
                                  description)
        return transaction

    def deposit(self, amount: Decimal, description='') -> bool:
        if not (isinstance(amount, Decimal) and isinstance(description, str)):
            print("Wrong argument assigned")
            return False
        # Transaction creation start
        transaction = self.__create_transaction('Deposit', amount, description)
        # Transaction creation end

        # Auditing start
        self.__transactions[transaction.get_id()] = transaction
        # Auditing end

        if amount <= Decimal('0.0'):  # Amount validation
            transaction.status_change_to_cancelled(3)  # Pending -> Cancelled
            return False

        self.__add_balance(amount)
        transaction.status_change_to_processed()
        # Pending -> Processed
        transaction.print_transaction_result(self.__current_balance)
        return True

    def withdraw(self, amount: Decimal, description='') -> bool:
        if not (isinstance(amount, Decimal) and isinstance(description, str)):
            print("Wrong argument assigned")
            return False
        # Transaction creation start
        transaction = self.__create_transaction(
            "Withdrawal", amount, description)
        # Transaction creation end

        # Auditing start
        self.__transactions[transaction.get_id()] = transaction
        # Auditing end

        if amount <= Decimal('0.0'):  # Amount validation
            transaction.status_change_to_cancelled(3)  # Pending -> Cancelled
            return False

        if self.__current_balance >= amount:  # checking balance
            self.__remove_balance(amount)
            transaction.status_change_to_processed()
            # Pending -> Processed
            transaction.print_transaction_result(self.__current_balance)
            return True

        else:
            transaction.status_change_to_cancelled(0)
            # Pending -> Cancelled
            return False

    def transfer(self, remittee, amount: Decimal, description='') -> bool:
        if not isinstance(amount, Decimal):
            print("Wrong argument assigned in \"amount\"")
            return False
        if not isinstance(description, str):
            print("Wrong argument assigned in \"description\"")
            return False
        if not isinstance(remittee, Account):
            print("Wrong argument assigned in \"remittee\"")
            return False
        # Transaction creation start
        transaction = self.__create_transaction(
            "Transfer", amount, description)
        transaction.set_remittee_account(remittee)
        transaction.set_remitter_account(self)
        # Transaction creation end

        # Auditing start
        self.__transactions[transaction.get_id()] = transaction
        # Auditing end

        if amount <= Decimal('0.0'):  # Amount validation
            transaction.status_change_to_cancelled(3)  # Pending -> Cancelled
            return False

        # Checking if matching receiver account does not exist.
        if remittee is None:
            transaction.status_change_to_cancelled(1)  # Pending -> Cancelled
            return False
        if self.__current_balance >= amount:  # checking balance
            receiver_balance = remittee.get_balance()
            remittee.receive(transaction)
            if remittee.get_balance() != receiver_balance + amount:
                # Reinstate remittee's balance
                remittee.remittee_transfer_rollback(
                    transaction, receiver_balance)
                transaction.status_change_to_cancelled(2)
                # Pending -> Cancelled
                return False
            self.__remove_balance(amount)
            transaction.status_change_to_processed()  # Pending -> Processed
            transaction.print_transaction_result(self.__current_balance, self)
            transaction.print_transaction_result(remittee.get_balance(),
                                                 remittee)
            # Pending -> Processed
            return True
        else:
            transaction.status_change_to_cancelled(0)  # Pending -> Cancelled
            return False

    # The helper method of receive()
    def __receive(self, transaction: Transaction):
        self.__add_balance(transaction.get_amount())
        self.__transactions[transaction.get_id()] = transaction

    def receive(self, transaction: Transaction):
        # To prevent someone puts fake arguments and exploits the system
        if isinstance(transaction, Transaction):
            if self is transaction.get_remittee():
                if transaction.get_type() == 'Transfer':
                    if transaction.get_status() == 'Pending':
                        self.__receive(transaction)

    # The helper method of remittee_transfer_rollback()
    def __remittee_transfer_rollback(self, rollback_balance):
        self.__current_balance = rollback_balance

    def remittee_transfer_rollback(self, transaction: Transaction, rollback_balance):
        # To prevent someone puts fake arguments and exploits the system
        if isinstance(transaction, Transaction):
            if self is transaction.get_remittee():
                if transaction.get_type() == 'Transfer':
                    if transaction.get_status() == 'Pending':
                        self.__remittee_transfer_rollback(rollback_balance)
