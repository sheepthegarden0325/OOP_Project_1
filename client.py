from account import Account


class Client:
    # Client has ID, name, contact_number, and a dictionary of accounts so that they can easily access to their bank account
    def __init__(self, id: int, name: str, contact_number: str, email: str):
        self.id = id
        self.name = name
        self.contact_number = contact_number
        self.email = email
        self.preferred_contact_method = "email"
        self.accounts = {  # this dictionary is for tracking client's accounts
            # "account_number": account_instance
        }

    # just for printing accounts but later I will use it for checking status.
    def check_account(self):
        print(self.accounts)

    # this method returns the exact account instance
    def access_acccount(self, account_number: str) -> Account:
        return self.accounts[account_number]

    def open_new_account(self, account_number):  # create a new account
        # I will need a line for checking whether the assigned account number is duplicated
        account = Account(self.id, account_number)
        self.accounts[account_number] = account

    # this take string values among name, contact_number, and email
    def contact_info_change(self, want_to_change_this: str, to_this: str):
        if want_to_change_this == "name":
            # input is too tricky to debug at some points FIX IT
            self.name = to_this
        elif want_to_change_this == "contact_number":
            self.contact_number = to_this
        else:
            self.email = to_this
