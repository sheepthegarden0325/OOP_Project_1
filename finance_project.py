import datetime


class Client:
    # Client has ID, name, contact_number, and a dictionary of accounts so that they can easily access to their bank account
    def __init__(self, id, name, contact_number, email):
        self.client_id = id
        self.client_name = name
        self.client_contact_number = contact_number
        self.client_email = email
        self.client_preferred_contact_method = "email"
        self.client_accounts = {  # this dictionary is for tracking client's accounts
            # "account_number": account_instance
        }

    # just for printing accounts but later I will use it for checking status.
    def check_account(self):
        print(self.client_accounts)

    # this method returns the exact account instance
    def access_acccount(self, account_number):
        return self.client_acccounts[account_number]

    def open_new_account(self, account_number):  # create a new account
        # I will need a line for checking whether the assigned account number is duplicated
        account = Account(self.client_id, account_number)
        self.client_accounts[account_number] = account

    # this take string values among name, contact_number, and email
    def contact_info_change(self, want_to_change_this):
        if want_to_change_this == "name":
            # input is too tricky to debug at some points FIX IT
            self.client_name = input("Please enter your name: ")
        elif want_to_change_this == "contact_number":
            self.client_contact_number = input(
                "Please enter your contact number: ")
        else:
            self.client_email = input("Please enter your email address: ")


class Account:
    def __init__(self, client_id, account_number):
        self.account_number = account_number
        self.clinet_id = client_id
        self.transaction_records = []
        self.current_balance = 0.0

    def add_balance(self, added_amount):
        self.current_balance += added_amount

    def remove_balace(self, removed_amount):
        self.current_balance -= removed_amount

    def deposit(self, deposit_amount):
        self.add_balance(deposit_amount)
        self.transaction_records.append({"date_time": datetime.now(
        ), "transaction_type": "deposit", "amount": deposit_amount})
        print(f"Date & Time: {datetime.now()} Transaction succeeded, Transaction type: deposit, Amount: ${deposit_amount}, Current balance: {self.current_balance}")

    def withdraw(self, withdrawal_amount):
        if self.current_balance >= withdrawal_amount:  # checking balance
            self.remove_balace(withdrawal_amount)
            self.transaction_records.append({"date_time": datetime.now(
            ), "transaction_type": "withdrawal", "amount": withdrawal_amount})
            print(
                f"Date & Time: {datetime.now()} Transaction succeeded, Transaction type: withdrawal, Amount: ${withdrawal_amount}, Current balance: {self.current_balance}")

        else:
            print("Transaction failed: not enough balance")

    def transfer(self, transfer_to_this_account, transferred_amount):
        if self.current_balance >= transferred_amount:  # checking balance
            self.remove_balace(transferred_amount)
            self.transaction_records.append({"date_time": datetime.now(
            ), "transaction_type": "transfer", "transfer_to_this_account": transfer_to_this_account, "amount": transferred_amount})
            print(f"Date & Time: {datetime.now()} Transaction succeeded, Transaction type: transfer, Receiver: {transfer_to_this_account}, Amount: ${transferred_amount}, Current balance: {self.current_balance}")

        else:
            print("Transaction failed: not enough balance")

    def receive(self, received_from_this_account, received_amount):
        self.add_balance(received_amount)
        self.transaction_records.append({"date_time": datetime.now(), "transaction_type": "transfer",
                                        "received_from_this_account": received_from_this_account, "amount": received_amount})
        print(f"Date & Time: {datetime.now()} Transaction succeeded, Transaction type: transfer, Remitee: {received_from_this_account}, Amount: ${received_amount}, Current balance: {self.current_balance}")
