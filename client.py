from account import Account
from bank import Bank


class Client:
    __next_id = 1
    # Client has ID, name, contact_number, and a dictionary of accounts so that they can easily access to their bank account

    def __init__(self, name: str, contact_number: str, email: str):
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
        self.__accounts = {  # this dictionary is for tracking client's accounts
            # "account_number": account_instance
        }
        Bank.add_client(self)

    # just for printing accounts but later I will use it for checking status.
    def check_account(self):
        print(self.__accounts)

    # this method returns the exact account instance
    def access_account(self, account_number: int):
        return self.__accounts[account_number]

    def get_id(self):
        return self.__id

    '''def open_new_account(self, account_number):  # create a new account
        # I will need a line for checking whether the assigned account number is duplicated
        account = Account(self.__id, account_number)
        self.__accounts[account_number] = account'''

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
