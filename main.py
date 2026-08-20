from client import Client
from account import Account
from decimal import Decimal
from branch import Branch

client_1 = Client("John", "0400-000-000", "test@email.com")
client_2 = Client("Jacob", "0401-000-000", "test@email.com")
client_1_account_1 = Account(client_1)
client_2_account_1 = Account(client_2)
client_1_account_2 = Account(client_1)
client_1.check_account()
client_2.check_account()

client_1_account_1.deposit(Decimal('100.0'))
client_1_account_1.transfer(client_2_account_1, Decimal('50.0'))
client_1_account_1.print_balance()
client_2_account_1.print_balance()

st_clair_westpac = Branch('WestPac St Clair', 'St Clair', '123456789')

st_clair_westpac.open()
st_clair_westpac.set_phone_number('000000000')
st_clair_westpac.close()
