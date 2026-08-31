from client import Client
from account import Account
from decimal import Decimal
from branch import Branch


# Object creation tests
client_1 = Client(
    "John",
    "0400-000-000",
    "test@email.com"
)
client_2 = Client(
    "Jacob",
    "0401-000-000",
    "test@email.com"
)

client_1_account_1 = Account(client_1)
client_1_account_2 = Account(client_1)
client_2_account_1 = Account(client_2)

branch_1 = Branch(
    'WestPac St Clair',
    'St Clair',
    '123456789'
)


print(client_1)
print(repr(client_1))

print(client_2)
print(repr(client_2))

print(client_1_account_1)
print(repr(client_1_account_1))

print(branch_1)
print(repr(branch_1))

client_1.check_account()
client_2.check_account()

print(
    client_1.access_account(
        client_1_account_1.get_number()
    ) is client_1_account_1
)

# Deposit tests
deposit_result = client_1_account_1.deposit(
    Decimal('100.00'),
    'Initial deposit'
)
print(f'Deposit result: {deposit_result}')
client_1_account_1.print_balance()

deposit_result = client_1_account_1.deposit(
    50,
    'Invalid deposit'
)
print(f'Deposit result: {deposit_result}')
client_1_account_1.print_balance()

deposit_result = client_1_account_1.deposit(
    Decimal('0.00')
)
print(f'Deposit result: {deposit_result}')
client_1_account_1.print_balance()

deposit_result = client_1_account_1.deposit(
    Decimal('-10.00')
)
print(f'Deposit result: {deposit_result}')
client_1_account_1.print_balance()

deposit_result = client_1_account_1.deposit(
    Decimal('10.00'),
    123
)
print(f'Deposit result: {deposit_result}')
client_1_account_1.print_balance()


# Withdrawal tests
withdrawal_result = client_1_account_1.withdraw(
    Decimal('30.00'),
    'Cash withdrawal'
)
print(f'Withdrawal result: {withdrawal_result}')
client_1_account_1.print_balance()

withdrawal_result = client_1_account_1.withdraw(
    Decimal('100.00')
)
print(f'Withdrawal result: {withdrawal_result}')
client_1_account_1.print_balance()

withdrawal_result = client_1_account_1.withdraw(
    Decimal('0.00')
)
print(f'Withdrawal result: {withdrawal_result}')
client_1_account_1.print_balance()

withdrawal_result = client_1_account_1.withdraw(
    Decimal('-10.00')
)
print(f'Withdrawal result: {withdrawal_result}')
client_1_account_1.print_balance()

withdrawal_result = client_1_account_1.withdraw(
    10
)
print(f'Withdrawal result: {withdrawal_result}')
client_1_account_1.print_balance()


# Transfer tests
transfer_result = client_1_account_1.transfer(
    client_2_account_1,
    Decimal('20.00'),
    'Test transfer'
)
print(f'Transfer result: {transfer_result}')
client_1_account_1.print_balance()
client_2_account_1.print_balance()

transfer_result = client_1_account_1.transfer(
    client_2_account_1,
    Decimal('100.00')
)
print(f'Transfer result: {transfer_result}')
client_1_account_1.print_balance()
client_2_account_1.print_balance()

transfer_result = client_1_account_1.transfer(
    client_2_account_1,
    Decimal('0.00')
)
print(f'Transfer result: {transfer_result}')
client_1_account_1.print_balance()
client_2_account_1.print_balance()

transfer_result = client_1_account_1.transfer(
    client_2_account_1,
    Decimal('-10.00')
)
print(f'Transfer result: {transfer_result}')
client_1_account_1.print_balance()
client_2_account_1.print_balance()

transfer_result = client_1_account_1.transfer(
    'Not an account',
    Decimal('10.00')
)
print(f'Transfer result: {transfer_result}')
client_1_account_1.print_balance()
client_2_account_1.print_balance()

transfer_result = client_1_account_1.transfer(
    client_2_account_1,
    10
)
print(f'Transfer result: {transfer_result}')
client_1_account_1.print_balance()
client_2_account_1.print_balance()

transfer_result = client_1_account_1.transfer(
    client_2_account_1,
    Decimal('10.00'),
    123
)
print(f'Transfer result: {transfer_result}')
client_1_account_1.print_balance()
client_2_account_1.print_balance()


# Client tests
print(client_1)

client_1.set_name('John Smith')
client_1.set_contact_number('0499-999-999')
client_1.set_email('john.smith@email.com')

print(client_1)
print(repr(client_1))

client_1.set_name(123)
client_1.set_contact_number(123)
client_1.set_email(123)

print(client_1)

client_1.remove_account(client_1_account_2)
client_1.check_account()

client_1.add_account(client_1_account_2)
client_1.check_account()


# Branch tests
print(branch_1)
print(repr(branch_1))

branch_1.open()
print(branch_1)

branch_1.set_phone_number('000000000')
print(branch_1)

branch_1.set_phone_number(123)
print(branch_1)

branch_1.close()
print(branch_1)
print(repr(branch_1))
