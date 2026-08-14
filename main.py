from account import Account
from client import Client
from bank import Bank

bank = Bank()

client_1 = bank.create_new_client(1, "John", "0400-000-000", "test@email.com")
client_1_account_1 = bank.open_new_account(client_1, "000-001")
bank.add_new_account(client_1.access_acccount('000-001'))
client_1.check_account()


client_1_account_1.deposit(100.0)
client_1_account_1.deposit(100.0)
