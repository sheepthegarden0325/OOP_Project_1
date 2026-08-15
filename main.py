from bank import Bank
from decimal import Decimal

bank = Bank()

client_1 = bank.create_new_client(1, "John", "0400-000-000", "test@email.com")
client_2 = bank.create_new_client(2, "Jacob", "0401-000-000", "test@email.com")
client_1_account_1 = bank.open_new_account(client_1, "000-001")
client_2_account_1 = bank.open_new_account(client_2, '000-002')
client_1.check_account()
client_2.check_account()

client_1_account_1.deposit(bank, Decimal('100.0'))
client_1_account_1.transfer(
    bank, bank.access_account('000-002'), Decimal('-50.0'))
client_1_account_1.print_balance()
client_2_account_1.print_balance()

st_clair_westpac = bank.open_new_branch(
    1, 'WestPac St Clair', 'St Clair', '123456789')

st_clair_westpac.open()
st_clair_westpac.update_phone_number('000000000')
st_clair_westpac.close()
