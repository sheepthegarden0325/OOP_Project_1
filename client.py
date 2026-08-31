from account import Account
from branch import Branch


class Client:
    """Store a client's details, accounts, and preferred branch.

    Attributes
    ----------
    __next_id : int
        The next available client ID.
    __id : int
        The client's unique ID.
    __name : str or None
        The client's name.
    __contact_number : str or None
        The client's contact number.
    __email : str or None
        The client's email address.
    __preferred_contact_method : str or None
        The client's preferred contact method.
    __accounts : dict
        The client's accounts, stored by account number.
    __preferred_branch : Branch or None
        The client's preferred branch.

    Methods
    -------
    __str__()
        Return readable client information.
    __repr__()
        Return detailed client information.
    set_preferred_branch(branch)
        Set the preferred branch if the object is a Branch.
    get_preferred_branch()
        Return the preferred branch or None.
    check_account()
        Print the client's accounts.
    access_account(account_number)
        Return the account with the given account number.
    get_id()
        Return the client ID.
    __add_account(account)
        Add an account to the client's accounts.
    add_account(account)
        Check and add an account.
    __remove_account(account)
        Remove an account from the client's accounts.
    remove_account(account)
        Check and remove an account.
    set_name(name)
        Update the client's name.
    set_contact_number(contact_number)
        Update the client's contact number.
    set_email(email)
        Update the client's email address.
    """

    __next_id = 1

    def __init__(self, name: str, contact_number: str, email: str):
        """Create a client without accounts or a preferred branch.

        Parameters
        ----------
        name : str
            The client's name.
        contact_number : str
            The client's contact number.
        email : str
            The client's email address.
        """
        self.__id = Client.__next_id
        Client.__next_id += 1

        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = None

        if isinstance(contact_number, str):
            self.__contact_number = contact_number
        else:
            self.__contact_number = None

        if isinstance(email, str):
            self.__email = email
        else:
            self.__email = None

        if self.__email is not None:
            self.__preferred_contact_method = "email"
        else:
            self.__preferred_contact_method = None

        self.__accounts = {}
        self.__preferred_branch = None

    def __str__(self):
        return (
            f'Client ID: {self.__id}, '
            f'Name: {self.__name}, '
            f'Contact number: {self.__contact_number}, '
            f'Email: {self.__email}, '
            f'Preferred contact method: '
            f'{self.__preferred_contact_method}, '
            f'Preferred branch: {self.__preferred_branch}, '
            f'Number of accounts: {len(self.__accounts)}'
        )

    def __repr__(self):
        return (
            f'Client('
            f'id={self.__id!r}, '
            f'name={self.__name!r}, '
            f'contact_number={self.__contact_number!r}, '
            f'email={self.__email!r}, '
            f'preferred_contact_method='
            f'{self.__preferred_contact_method!r}, '
            f'preferred_branch={self.__preferred_branch!r}, '
            f'account_numbers={list(self.__accounts)!r})'
        )

    def set_preferred_branch(self, branch: Branch):
        if isinstance(branch, Branch):
            self.__preferred_branch = branch

    def get_preferred_branch(self) -> Branch:
        return self.__preferred_branch

    # TODO: Update this method to print each account's status.
    def check_account(self):
        print(self.__accounts)

    # this method returns the exact account instance
    def access_account(self, account_number: int):
        return self.__accounts[account_number]

    def get_id(self):
        return self.__id

    def __add_account(self, account):
        self.__accounts[account.get_number()] = account

    def add_account(self, account: Account):
        if isinstance(account, Account):  # input validation
            # To prevent adding a redundant account
            if account.get_number() not in self.__accounts:
                self.__add_account(account)

    def __remove_account(self, account: Account):
        del self.__accounts[account.get_number()]

    def remove_account(self, account: Account):
        if isinstance(account, Account):
            if account.get_number() in self.__accounts:
                self.__remove_account(account)

    def set_name(self, name):
        if not isinstance(name, str):
            print("Worng name argument")
        else:
            self.__name = name

    def set_contact_number(self, contact_number):
        if not isinstance(contact_number, str):
            print("Worng contact number argument")
        else:
            self.__contact_number = contact_number

    def set_email(self, email):
        if not isinstance(email, str):
            print("Worng email argument")
        else:
            self.__email = email
