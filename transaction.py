from datetime import datetime


class Transaction:

    def __init__(self, id, type, amount, description):
        self.id = id
        self.date_time = datetime.now()
        self.type = type
        self.amount = amount
        self.description = description
        self.sender_account = ''
        self.receiver_account = ''
        self.status = 'Pending'

    def status_change_to_processed(self, current_balance):
        if self.status == 'Pending':
            self.status = 'Processed'
            self.date_time = datetime.now()
            if self.type == 'deposit':
                print(
                    f"Date & Time: {datetime.now()} Transaction succeeded, Transaction type: deposit, Amount: ${self.amount}, Current balance: {current_balance}")
            elif self.type == 'withdrawal':
                print(
                    f"Date & Time: {datetime.now()} Transaction succeeded, Transaction type: withdrawal, Amount: ${self.amount}, Current balance: {current_balance}")
            elif self.type == 'transfer':
                print
            else:
                print
        else:
            return 'Failed'

    def status_change_to_cancelled(self):
        if self.status == "Pending":
            self.status = "Cancelled"
            self.date_time = datetime.now()
            if self.status == 'withdrawal':
                print("Transaction failed: Not enough balance")
        else:
            return 'Failed'

    def update_transaction_description(self, description: str):
        self.description = description
