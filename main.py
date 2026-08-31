from client import Client
from account import Account
from decimal import Decimal
from branch import Branch


# Create multiple objects to test interactions between the classes.
client_1 = Client(
    'John',
    '0400-000-000',
    'test@email.com'
)
client_2 = Client(
    'Jacob',
    '0401-000-000',
    'jacob@email.com'
)

client_1_account_1 = Account(client_1)
client_1_account_2 = Account(client_1)
client_2_account_1 = Account(client_2)

branch_1 = Branch(
    'WestPac St Clair',
    'St Clair',
    '123456789'
)
branch_2 = Branch(
    'WestPac Adelaide',
    'Adelaide',
    '987654321'
)


print('\n=== Object creation tests ===')

print(client_1)
print(repr(client_1))

print(client_2)
print(repr(client_2))

print(client_1_account_1)
print(repr(client_1_account_1))

print(client_1_account_2)
print(repr(client_1_account_2))

print(client_2_account_1)
print(repr(client_2_account_1))

print(branch_1)
print(repr(branch_1))

print(branch_2)
print(repr(branch_2))

print(
    f'Client IDs are different: '
    f'{client_1.get_id() != client_2.get_id()}'
)
print(
    f'Account numbers are different: '
    f'{client_1_account_1.get_number() != client_1_account_2.get_number()}'
)
print(
    f'Branch numbers are different: '
    f'{branch_1.get_number() != branch_2.get_number()}'
)


print('\n=== Client and Account relationship tests ===')

client_1.check_account()
client_2.check_account()

accessed_account = client_1.access_account(
    client_1_account_1.get_number()
)

print(
    f'Correct account returned: '
    f'{accessed_account is client_1_account_1}'
)

# Removing and adding an account tests the aggregation methods.
client_1.remove_account(client_1_account_2)
client_1.check_account()
print('Expected number of accounts: 1')
print(client_1)

client_1.add_account(client_1_account_2)
client_1.check_account()
print('Expected number of accounts: 2')
print(client_1)

# Adding the same account again should not create a duplicate.
client_1.add_account(client_1_account_2)
client_1.check_account()
print('Expected number of accounts after duplicate attempt: 2')
print(client_1)

# Invalid objects should not change the client's accounts.
client_1.add_account('Not an account')
client_1.remove_account('Not an account')
client_1.check_account()
print('Expected number of accounts after invalid attempts: 2')
print(client_1)


print('\n=== Preferred Branch tests ===')

print(
    f'Initial preferred branch is None: '
    f'{client_1.get_preferred_branch() is None}'
)

client_1.set_preferred_branch(branch_1)
print(
    f'Preferred branch set correctly: '
    f'{client_1.get_preferred_branch() is branch_1}'
)
print(client_1)

# Setting another branch should change the preferred branch.
client_1.set_preferred_branch(branch_2)
print(
    f'Preferred branch changed correctly: '
    f'{client_1.get_preferred_branch() is branch_2}'
)
print(client_1)

# An invalid object should not replace the preferred branch.
client_1.set_preferred_branch('Not a branch')
print(
    f'Invalid branch was rejected: '
    f'{client_1.get_preferred_branch() is branch_2}'
)
print(client_1)


print('\n=== Deposit tests ===')

# Account creates and processes its transactions internally.
deposit_result = client_1_account_1.deposit(
    Decimal('100.00'),
    'Initial deposit'
)
print(f'Deposit result: {deposit_result} (expected: True)')
client_1_account_1.print_balance()
print('Expected balance: 100.00')

deposit_result = client_1_account_1.deposit(
    50,
    'Invalid deposit'
)
print(f'Deposit result: {deposit_result} (expected: False)')
client_1_account_1.print_balance()
print('Expected balance: 100.00')

deposit_result = client_1_account_1.deposit(
    Decimal('0.00')
)
print(f'Deposit result: {deposit_result} (expected: False)')
client_1_account_1.print_balance()
print('Expected balance: 100.00')

deposit_result = client_1_account_1.deposit(
    Decimal('-10.00')
)
print(f'Deposit result: {deposit_result} (expected: False)')
client_1_account_1.print_balance()
print('Expected balance: 100.00')

deposit_result = client_1_account_1.deposit(
    Decimal('10.00'),
    123
)
print(f'Deposit result: {deposit_result} (expected: False)')
client_1_account_1.print_balance()
print('Expected balance: 100.00')


print('\n=== Withdrawal tests ===')

withdrawal_result = client_1_account_1.withdraw(
    Decimal('30.00'),
    'Cash withdrawal'
)
print(f'Withdrawal result: {withdrawal_result} (expected: True)')
client_1_account_1.print_balance()
print('Expected balance: 70.00')

withdrawal_result = client_1_account_1.withdraw(
    Decimal('100.00')
)
print(f'Withdrawal result: {withdrawal_result} (expected: False)')
client_1_account_1.print_balance()
print('Expected balance: 70.00')

withdrawal_result = client_1_account_1.withdraw(
    Decimal('0.00')
)
print(f'Withdrawal result: {withdrawal_result} (expected: False)')
client_1_account_1.print_balance()
print('Expected balance: 70.00')

withdrawal_result = client_1_account_1.withdraw(
    Decimal('-10.00')
)
print(f'Withdrawal result: {withdrawal_result} (expected: False)')
client_1_account_1.print_balance()
print('Expected balance: 70.00')

withdrawal_result = client_1_account_1.withdraw(
    10
)
print(f'Withdrawal result: {withdrawal_result} (expected: False)')
client_1_account_1.print_balance()
print('Expected balance: 70.00')

withdrawal_result = client_1_account_1.withdraw(
    Decimal('10.00'),
    123
)
print(f'Withdrawal result: {withdrawal_result} (expected: False)')
client_1_account_1.print_balance()
print('Expected balance: 70.00')


print('\n=== Transfer tests ===')

transfer_result = client_1_account_1.transfer(
    client_2_account_1,
    Decimal('20.00'),
    'Test transfer'
)
print(f'Transfer result: {transfer_result} (expected: True)')
client_1_account_1.print_balance()
client_2_account_1.print_balance()
print('Expected remitter balance: 50.00')
print('Expected remittee balance: 20.00')

transfer_result = client_1_account_1.transfer(
    client_2_account_1,
    Decimal('100.00')
)
print(f'Transfer result: {transfer_result} (expected: False)')
client_1_account_1.print_balance()
client_2_account_1.print_balance()
print('Expected remitter balance: 50.00')
print('Expected remittee balance: 20.00')

transfer_result = client_1_account_1.transfer(
    client_2_account_1,
    Decimal('0.00')
)
print(f'Transfer result: {transfer_result} (expected: False)')
client_1_account_1.print_balance()
client_2_account_1.print_balance()

transfer_result = client_1_account_1.transfer(
    client_2_account_1,
    Decimal('-10.00')
)
print(f'Transfer result: {transfer_result} (expected: False)')
client_1_account_1.print_balance()
client_2_account_1.print_balance()

transfer_result = client_1_account_1.transfer(
    'Not an account',
    Decimal('10.00')
)
print(f'Transfer result: {transfer_result} (expected: False)')
client_1_account_1.print_balance()
client_2_account_1.print_balance()

transfer_result = client_1_account_1.transfer(
    client_2_account_1,
    10
)
print(f'Transfer result: {transfer_result} (expected: False)')
client_1_account_1.print_balance()
client_2_account_1.print_balance()

transfer_result = client_1_account_1.transfer(
    client_2_account_1,
    Decimal('10.00'),
    123
)
print(f'Transfer result: {transfer_result} (expected: False)')
client_1_account_1.print_balance()
client_2_account_1.print_balance()

print('Expected final remitter balance: 50.00')
print('Expected final remittee balance: 20.00')


print('\n=== Rollback validation test ===')

# An unrelated value must not be able to change the account balance.
balance_before_rollback = client_2_account_1.get_balance()

client_2_account_1.remittee_transfer_rollback(
    'Not a transaction',
    Decimal('0.00')
)

print(
    f'Invalid rollback was rejected: '
    f'{client_2_account_1.get_balance() == balance_before_rollback}'
)


print('\n=== Client detail tests ===')

print(client_1)

client_1.set_name('John Smith')
client_1.set_contact_number('0499-999-999')
client_1.set_email('john.smith@email.com')

print(client_1)
print(repr(client_1))

# Invalid values should not replace valid client details.
client_1.set_name(123)
client_1.set_contact_number(123)
client_1.set_email(123)

print(client_1)
print('Expected name: John Smith')
print('Expected contact number: 0499-999-999')
print('Expected email: john.smith@email.com')


print('\n=== Branch tests ===')

print(branch_1)
print(repr(branch_1))

branch_1.open()
print(branch_1)
print('Expected status: Open')

branch_1.set_phone_number('000000000')
print(branch_1)
print('Expected phone number: 000000000')

# An invalid phone number should not replace the valid number.
branch_1.set_phone_number(123)
print(branch_1)
print('Expected phone number after invalid attempt: 000000000')

branch_1.close()
print(branch_1)
print(repr(branch_1))
print('Expected status: Closed')
