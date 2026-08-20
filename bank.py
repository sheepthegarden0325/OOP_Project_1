
class Bank:  # This class exists for efficiently retrieving and accsessing accounts and clients.

    __clients = {
        # client_id: Client
    }
    __accounts = {
        # account_id: Account
    }
    __transactions = {
        # transaction_id: Transaction
    }
    __branches = {
        # branch_id: Branch
    }

    def __init__(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass
        # it was for the central control model, but it is not necessary now
    '''def create_new_client(self, client_id: int, client_name: str, client_contact_number: str, client_email: str) -> Client:

        if client_id in self.__clients:
            print("ERROR: This client ID already exists.")
            return

        client = Client(client_id,
                        client_name,
                        client_contact_number,
                        client_email)
        self.__clients[client_id] = client
        return client

    def open_new_account(self, client: Client, account_number: str) -> Account:

        if account_number in self.__accounts:
            print("ERROR: This account number is already occupied.")
            return

        account = Account(client, account_number)
        # cross-reference between Client and Account
        client.accounts[account_number] = account
        self.__accounts[account_number] = account
        return account

    def open_new_branch(self, branch_number: int, branch_name: str, branch_suburb: str, branch_phone_number: str) -> Branch:
        branch = Branch(branch_number,
                        branch_name,
                        branch_suburb,
                        branch_phone_number)
        self.__branches[branch_number] = branch
        return branch'''
    @classmethod
    def add_client(self, client):
        Bank.__clients[client.get_id()] = client

    @classmethod
    def add_account(self, account):
        Bank.__accounts[account.get_number()] = account

    @classmethod
    def add_transaction(self, transaction):
        Bank.__accounts[transaction.get_id()] = transaction

    @classmethod
    def add_branch(self, branch):
        Bank.__branches[branch.get_number()] = branch

    @classmethod
    def access_account(self, account_number):
        return Bank.__accounts.get(account_number)

    @classmethod
    def access_client(self, client_id):
        return Bank.__clients[client_id]

    @classmethod
    def access_transaction(self, transaction_id):
        return Bank.__transactions[transaction_id]

    @classmethod
    def access_branch(self, branch_number):
        return Bank.__branches[branch_number]
