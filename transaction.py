from datetime import datetime
from decimal import Decimal


class Transaction:
    """Store the details and status of a bank transaction.

    A transaction starts as Pending and can change to Processed or
    Cancelled.

    Attributes
    ----------
    __next_id : int
        The next available transaction ID.
    __id : int
        The transaction's unique ID.
    __date_time : datetime
        The time the transaction was created or updated.
    __type : str
        The transaction type.
    __amount : Decimal
        The transaction amount.
    __description : str
        A description of the transaction.
    __remitter_account : Account or None
        The account sending money in a transfer.
    __remittee_account : Account or None
        The account receiving money in a transfer.
    __status : str
        The transaction's current status.

    Methods
    -------
    __str__()
        Return readable transaction information.
    __repr__()
        Return detailed transaction information.
    status_change_to_processed()
        Change the status from Pending to Processed.
    status_change_to_cancelled(error_code)
        Change the status from Pending to Cancelled.
    print_transaction_result(current_balance, viewer_account=None)
        Print the result of the transaction.
    get_id()
        Return the transaction ID.
    get_remittee()
        Return the remittee account.
    get_amount()
        Return the transaction amount.
    get_type()
        Return the transaction type.
    get_status()
        Return the transaction status.
    set_description(description)
        Update the transaction description.
    """

    __next_id = 1

    def __init__(
            self,
            type,
            amount: Decimal,
            description: str,
            remitter=None,
            remittee=None):
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
            The account sending money in a transfer.
        remittee : Account, optional
            The account receiving money in a transfer.
        """

        self.__id = Transaction.__next_id
        Transaction.__next_id += 1
        self.__date_time = datetime.now()
        self.__type = type
        self.__amount = amount
        self.__description = description
        self.__remitter_account = remitter
        self.__remittee_account = remittee
        self.__status = 'Pending'

    def status_change_to_processed(self):
        """Change a pending transaction to Processed.

        Returns
        -------
        bool
            True if the pending transaction was processed;
            otherwise, False.
        """
        if self.__status == 'Pending':
            self.__status = 'Processed'
            self.__date_time = datetime.now()
            return True

        else:
            return False

    def __str__(self):
        transaction_information = (
            f'Date & Time: {self.__date_time}, '
            f'Transaction ID: {self.__id}, '
            f'Transaction status: {self.__status}, '
            f'Transaction type: {self.__type}, '
            f'Amount: ${self.__amount}'
        )

        if self.__type == 'Transfer':
            if self.__remitter_account is None:
                remitter_number = None
            else:
                remitter_number = (
                    self.__remitter_account.get_number()
                )

            if self.__remittee_account is None:
                remittee_number = None
            else:
                remittee_number = (
                    self.__remittee_account.get_number()
                )

            transaction_information += (
                f', Remitter: {remitter_number}, '
                f'Remittee: {remittee_number}'
            )

        if self.__description:
            transaction_information += (
                f', Description: {self.__description}'
            )

        return transaction_information

    def __repr__(self):
        if self.__remitter_account is None:
            remitter_number = None
        else:
            remitter_number = (
                self.__remitter_account.get_number()
            )

        if self.__remittee_account is None:
            remittee_number = None
        else:
            remittee_number = (
                self.__remittee_account.get_number()
            )

        return (
            f'Transaction('
            f'id={self.__id!r}, '
            f'date_time={self.__date_time!r}, '
            f'type={self.__type!r}, '
            f'amount={self.__amount!r}, '
            f'description={self.__description!r}, '
            f'remitter_number={remitter_number!r}, '
            f'remittee_number={remittee_number!r}, '
            f'status={self.__status!r})'
        )

    def status_change_to_cancelled(self, error_code: int):
        """Cancel a pending transaction and print the reason.

        Parameters
        ----------
        error_code : int
            The reason for cancelling the transaction:
            0 indicates a banking system calculation error.

        Returns
        -------
        bool
            True if the pending transaction was cancelled;
            otherwise, False.
        """

        if self.__status == "Pending":
            self.__status = "Cancelled"
            self.__date_time = datetime.now()
            if error_code == 0:
                print(
                    f"Date & Time: {self.__date_time}",
                    f"Transaction status: {self.__status}",
                    "Banking system calculation error."
                )
            return True

        else:
            return False

    def print_transaction_result(
            self,
            current_balance,
            viewer_account=None):
        """Print the result of a processed transaction.

        For a transfer, the amount is displayed as positive for the
        remittee and negative for the remitter.

        Parameters
        ----------
        current_balance : Decimal
            The account balance after the transaction.
        viewer_account : Account, optional
            The account viewing a transfer result.

        Returns
        -------
        None
        """
        if self.__type == 'Deposit':
            print(
                f"Date & Time: {self.__date_time}",
                f"Transaction status: {self.__status}",
                f"Transaction type: Deposit",
                f"Amount: + ${self.__amount}",
                f"Current balance: {current_balance}",
                sep=", "
            )
        elif self.__type == 'Withdrawal':
            print(
                f"Date & Time: {self.__date_time}",
                f"Transaction status: {self.__status}",
                "Transaction type: Withdrawal",
                f"Amount: - ${self.__amount}",
                f"Current balance: {current_balance}",
                sep=", "
            )
        elif self.__type == 'Transfer':
            if viewer_account is self.__remittee_account:
                print(
                    f'Date & Time: {self.__date_time}',
                    f'Transaction status: {self.__status}',
                    f'Transaction type: Transfer',
                    f'Remitter: {self.__remitter_account.get_number()}',
                    f'Remittee: {self.__remittee_account.get_number()}',
                    f'Amount: + ${self.__amount}',
                    f'Current balance: {current_balance}',
                    sep=", "
                )
            elif viewer_account is self.__remitter_account:
                print(
                    f"Date & Time: {self.__date_time}",
                    f"Transaction status: {self.__status}",
                    f"Transaction type: Transfer",
                    f"Remitter: {self.__remitter_account.get_number()}",
                    f"Remittee: {self.__remittee_account.get_number()}",
                    f"Amount: - ${self.__amount}",
                    f"Current balance: {current_balance}",
                    sep=", "
                )

    # ------------
    # Getters
    # ------------

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

    # ---------
    # Setter
    # ---------

    def set_description(self, description: str):
        """Update the transaction description.

        Parameters
        ----------
        description : str
            The new transaction description.
        """
        if isinstance(description, str):
            self.__description = description

    # ----------
    # Properties
    # ----------

    id = property(get_id)
    remittee = property(get_remittee)
    amount = property(get_amount)
    type = property(get_type)
    status = property(get_status)
    description = property(fset=set_description)
