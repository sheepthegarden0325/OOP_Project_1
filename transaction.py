from datetime import datetime
from decimal import Decimal
from bank import Bank


class Transaction:
    __next_id = 1

    def __init__(self, type, amount: Decimal, description):
        self.__id = Transaction.__next_id
        Transaction.__next_id += 1
        self.__date_time = datetime.now()
        self.__type = type
        self.__amount = amount
        self.__description = description
        self.__remitter_account = None
        self.__remittee_account = None
        self.__status = 'Pending'
        Bank.add_transaction(self)

    def status_change_to_processed(self):
        if self.__status == 'Pending':
            self.__status = 'Processed'
            self.__date_time = datetime.now()  # Time updates
            return True

        else:
            return False

    def status_change_to_cancelled(self, error_code: int):

        if self.__status == "Pending":
            self.__status = "Cancelled"
            self.__date_time = datetime.now()  # Time updates
            if error_code == 0:  # error_code: 0 -> Not enough balance
                print(
                    f"Date & Time: {datetime.now()}",
                    f"Transaction status: {self.__status}",
                    f"Not enough balance."
                )
            elif error_code == 1:  # error_code: 1 -> No matching receiver account
                print(
                    f"Date & Time: {datetime.now()}",
                    f"Transaction status: {self.__status}",
                    "No matching remittee account."
                )
            elif error_code == 2:  # error_code: 2 -> System failed adding exact amount of money on receiver account
                print(
                    f"Date & Time: {datetime.now()}",
                    f"Transaction status: {self.__status}",
                    "Banking system calculation error."
                )
            elif error_code == 3:  # error_code: 3 -> Wrong amount input
                print(
                    f"Date & Time: {datetime.now()}",
                    f"Transaction status: {self.__status}",
                    "Amount cannot be 0 or negative."
                )
            return True

        else:
            return False

    def print_transaction_result(self, current_balance, viewer_account=None):
        if self.__type == 'Deposit':
            print(
                f"Date & Time: {datetime.now()}",
                f"Transaction status: {self.__status}",
                f"Transaction type: Deposit",
                f"Amount: + ${self.__amount}",
                f"Current balance: {current_balance}",
                sep=", "
            )
        elif self.__type == 'Withdrawal':
            print(
                f"Date & Time: {datetime.now()}",
                f"Transaction status: {self.__status}",
                "Transaction type: Withdrawal",
                f"Amount: - ${self.__amount}",
                f"Current balance: {current_balance}",
                sep=", "
            )
        elif self.__type == 'Transfer':
            if viewer_account is self.__remittee_account:  # Message for remittee
                print(
                    f'Date & Time: {datetime.now()}',
                    f'Transaction status: {self.__status}',
                    f'Transaction type: Transfer',
                    f'Remitter: {self.__remitter_account.get_number()}',
                    f'Remittee: {self.__remittee_account.get_number()}',
                    f'Amount: + ${self.__amount}',
                    f'Current balance: {current_balance}',
                    sep=", "
                )
            elif viewer_account is self.__remitter_account:  # message for remitter
                print(
                    f"Date & Time: {datetime.now()}",
                    f"Transaction status: {self.__status}",
                    f"Transaction type: Transfer",
                    f"Remitter: {self.__remitter_account.get_number()}",
                    f"Remittee: {self.__remittee_account.get_number()}",
                    f"Amount: - ${self.__amount}",
                    f"Current balance: {current_balance}",
                    sep=", "
                )

    def get_id(self):
        return self.__id

    def get_remittee(self):
        return self.__remittee_account

    def get_amount(self):
        return self.__amount

    def get_type(self):
        return self.__type

    def get_status(self):
        return self.__status

    def set_description(self, description: str):
        if isinstance(description, str):
            self.__description = description

    def set_remitter_account(self, remitter):
        self.__remitter_account = remitter

    def set_remittee_account(self, remittee):
        self.__remittee_account = remittee
