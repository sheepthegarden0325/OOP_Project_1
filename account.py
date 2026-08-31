from datetime import datetime
from transaction import Transaction
from decimal import Decimal


class Account:
    """Manage a client's account balance and transactions.

    Attributes
    ----------
    __next_number : int
        The next available account number.
    __number : int
        The account's unique number.
    __transactions : dict
        The account's transactions, stored by transaction ID.
    __current_balance : Decimal
        The account's current balance.

    Methods
    -------
    get_number()
        Return the account number.
    get_balance()
        Return the current balance.
    deposit(amount, description='')
        Add money to the account.
    withdraw(amount, description='')
        Remove money from the account.
    transfer(remittee, amount, description='')
        Send money to another account.
    """

    __next_number = 1

    def __init__(self, client):
        """Create an account for a client.

        Parameters
        ----------
        client : Client
            The client who owns the account.
        """

        self.__number = Account.__next_number
        Account.__next_number += 1
        # Importing here prevents a circular import with the Client module.
        from client import Client

        if isinstance(client, Client):
            client.add_account(self)
        self.__transactions = {}
        self.__current_balance = Decimal('0.0')

    def __str__(self):
        return (
            f'Account number: {self.__number}, '
            f'Current balance: ${self.__current_balance:.2f}, '
            f'Number of transactions: {len(self.__transactions)}'
        )

    def __repr__(self):
        return (
            f'Account('
            f'number={self.__number!r}, '
            f'current_balance={self.__current_balance!r}, '
            f'transaction_ids={list(self.__transactions)!r})'
        )

    def get_number(self) -> int:
        return self.__number

    def get_balance(self) -> Decimal:
        return self.__current_balance

    def print_balance(self):
        """Print the account number and current balance."""
        print(
            f'Date & Time: {datetime.now()}',
            f'Account: {self.__number}',
            f'Current balance: {self.__current_balance}',
            sep=', '
        )
        return

    def __add_balance(self, added_amount):
        """Add an amount to the current balance."""
        self.__current_balance += added_amount

    def __remove_balance(self, removed_amount):
        """Remove an amount from the current balance."""
        self.__current_balance -= removed_amount

    def __create_transaction(
            self,
            type,
            amount,
            description,
            remitter=None,
            remittee=None) -> Transaction:
        """Create a pending transaction.

        Parameters
        ----------
        type : str
            The transaction type.
        amount : Decimal
            The transaction amount.
        description : str
            A description of the transaction.
        remitter : Account, optional
            The account sending money.
        remittee : Account, optional
            The account receiving money.

        Returns
        -------
        Transaction
            The new transaction.
        """
        transaction = Transaction(
            type,
            amount,
            description,
            remitter,
            remittee
        )
        return transaction

    def deposit(self, amount: Decimal, description='') -> bool:
        """Deposit money and record the transaction.

        Parameters
        ----------
        amount : Decimal
            The amount of money to deposit.
        description : str, optional
            A description of the deposit.

        Returns
        -------
        bool
            True if the deposit was processed; otherwise, False.
        """

        if not isinstance(amount, Decimal):
            if isinstance(description, str):
                print("Wrong argument assigned")
                return False

        transaction = self.__create_transaction(
            'Deposit',
            amount,
            description
        )

        self.__transactions[transaction.get_id()] = transaction

        if amount <= Decimal('0.0'):
            transaction.status_change_to_cancelled(3)
            return False

        self.__add_balance(amount)
        transaction.status_change_to_processed()
        transaction.print_transaction_result(self.__current_balance)
        return True

    def withdraw(self, amount: Decimal, description='') -> bool:
        """Withdraw money and record the transaction.

        Parameters
        ----------
        amount : Decimal
            The amount of money to withdraw.
        description : str, optional
            A description of the withdrawal.

        Returns
        -------
        bool
            True if the withdrawal was processed; otherwise, False.
        """
        if not (isinstance(amount, Decimal)
                and isinstance(description, str)):
            print("Wrong argument assigned")
            return False

        transaction = self.__create_transaction(
            "Withdrawal",
            amount,
            description
        )
        self.__transactions[transaction.get_id()] = transaction

        if amount <= Decimal('0.0'):
            transaction.status_change_to_cancelled(3)
            return False

        if self.__current_balance >= amount:
            self.__remove_balance(amount)
            transaction.status_change_to_processed()
            transaction.print_transaction_result(self.__current_balance)
            return True

        else:
            transaction.status_change_to_cancelled(0)
            return False

    def transfer(
            self,
            remittee,
            amount: Decimal,
            description='') -> bool:
        """Transfer money from this account to another account.

        Parameters
        ----------
        remittee : Account
            The account receiving the money.
        amount : Decimal
            The amount of money to transfer.
        description : str, optional
            A description of the transfer..

        Returns
        -------
        bool
            True if the transfer was processed; otherwise, False.
        """
        if not isinstance(amount, Decimal):
            print("Wrong argument assigned in \"amount\"")
            return False

        if not isinstance(description, str):
            print("Wrong argument assigned in \"description\"")
            return False

        if not isinstance(remittee, Account):
            print("Wrong argument assigned in \"remittee\"")
            return False

        transaction = self.__create_transaction(
            "Transfer",
            amount,
            description,
            self,
            remittee
        )

        self.__transactions[transaction.get_id()] = transaction

        if amount <= Decimal('0.0'):
            transaction.status_change_to_cancelled(3)
            return False

        if self.__current_balance >= amount:
            receiver_balance = remittee.get_balance()
            remittee.__receive(transaction)

            if remittee.get_balance() != receiver_balance + amount:
                remittee.remittee_transfer_rollback(
                    transaction, receiver_balance)

                transaction.status_change_to_cancelled(2)
                return False

            self.__remove_balance(amount)
            transaction.status_change_to_processed()
            transaction.print_transaction_result(self.__current_balance, self)
            transaction.print_transaction_result(
                remittee.get_balance(),
                remittee
            )
            return True

        else:
            transaction.status_change_to_cancelled(0)
            return False

    def __receive(self, transaction: Transaction):
        """Receive and record a transfer transaction.

        Parameters
        ----------
        transaction : Transaction
            The transfer transaction being received.
        """
        self.__add_balance(transaction.get_amount())
        self.__transactions[transaction.get_id()] = transaction

    def __remittee_transfer_rollback(self, rollback_balance):
        """Restore the balance recorded before a transfer."""
        self.__current_balance = rollback_balance

    def remittee_transfer_rollback(
        self,
        transaction: Transaction,
        rollback_balance
    ):
        """Check and restore the remittee's balance.

        Parameters
        ----------
        transaction : Transaction
            The transfer that needs to be rolled back.
        rollback_balance : Decimal
            The balance recorded before the transfer.
        """
        # Only the pending transfer's remittee can restore its balance.
        if isinstance(transaction, Transaction):
            if self is transaction.get_remittee():
                if transaction.get_type() == 'Transfer':
                    if transaction.get_status() == 'Pending':
                        self.__remittee_transfer_rollback(rollback_balance)
