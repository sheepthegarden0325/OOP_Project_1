from client import Client
from account import Account
from branch import Branch


class Bank:  # This class exists for efficiently retrieving and accsessing accounts and clients.

    def __init__(self):
        self.clients = {
            # client_id: Client
        }
        self.accounts = {
            # account_id: Account
        }
        self.transactions = {
            # transaction_id: Transaction
        }
        self.branches = {
            # branch_id: Branch
        }

    def create_new_client(self, client_id: int, client_name: str, client_contact_number: str, client_email: str) -> Client:

        if client_id in self.clients:
            print("ERROR: This client ID already exists.")
            return

        client = Client(client_id,
                        client_name,
                        client_contact_number,
                        client_email)
        self.clients[client_id] = client
        return client

    def open_new_account(self, client: Client, account_number: str) -> Account:

        if account_number in self.accounts:
            print("ERROR: This account number is already occupied.")
            return

        account = Account(client, account_number)
        # cross-reference between Client and Account
        client.accounts[account_number] = account
        self.accounts[account_number] = account
        return account

    def open_new_branch(self, branch_number: int, branch_name: str, branch_suburb: str, branch_phone_number: str) -> Branch:
        branch = Branch(branch_number,
                        branch_name,
                        branch_suburb,
                        branch_phone_number)
        self.branches[branch_number] = branch
        return branch

    def access_account(self, account_number) -> Account:
        return self.accounts.get(account_number)

    def access_client(self, client_id) -> Client:
        return self.clients[client_id]

    def access_transaction(self, transaction_id):
        return self.transactions[transaction_id]

    def access_branch(self, branch_number) -> Branch:
        return self.branches[branch_number]
