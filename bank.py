from client import Client
from account import Account


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
