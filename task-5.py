
from decimal import Decimal, InvalidOperation


class ATM:
    def __init__(
        self,
        account_holder,
        initial_balance=Decimal("1000.00"),
        daily_withdrawal_limit=Decimal("20000.00"),
        max_deposit=Decimal("50000.00"),
        max_withdrawal=Decimal("10000.00"),
    ):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        if min(daily_withdrawal_limit, max_deposit, max_withdrawal) <= 0:
            raise ValueError("Transaction limits must be positive.")

        self.account_holder = account_holder
        self.balance = initial_balance
        self.daily_withdrawal_limit = daily_withdrawal_limit
        self.max_deposit = max_deposit
        self.max_withdrawal = max_withdrawal

        self.total_withdrawn_today = Decimal("0.00")
        self.transactions = []

    @staticmethod
    def read_amount(prompt):
        """Read and validate a positive monetary amount."""
        try:
            amount = Decimal(input(prompt).strip())

            if not amount.is_finite():
                raise ValueError("Amount must be a finite number.")

            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")

            if amount.as_tuple().exponent < -2:
                raise ValueError(
                    "Amount cannot have more than two decimal places."
                )

            return amount

        except InvalidOperation:
            raise ValueError("Please enter a valid numeric amount.")

    def record_transaction(self, transaction_type, amount, note=""):
        self.transactions.append({
            "type": transaction_type,
            "amount": amount,
            "balance": self.balance,
            "note": note,
        })

    def deposit(self):
        try:
            amount = self.read_amount("Enter deposit amount: ₹")

            if amount > self.max_deposit:
                print(
                    f"Deposit exceeds the per-transaction limit "
                    f"of ₹{self.max_deposit:.2f}."
                )
                return

            self.balance += amount
            self.record_transaction("Deposit", amount)

            print(f"Deposit successful: ₹{amount:.2f}")
            print(f"Available balance: ₹{self.balance:.2f}")

        except ValueError as error:
            print("Error:", error)

    def withdraw(self):
        try:
            amount = self.read_amount("Enter withdrawal amount: ₹")

            if amount > self.max_withdrawal:
                print(
                    f"Withdrawal exceeds the per-transaction limit "
                    f"of ₹{self.max_withdrawal:.2f}."
                )
                return

            if amount > self.balance:
                print("Transaction declined: Insufficient balance.")
                return

            remaining_limit = (
                self.daily_withdrawal_limit
                - self.total_withdrawn_today
            )

            if amount > remaining_limit:
                print(
                    "Transaction declined: Daily withdrawal limit "
                    f"remaining is ₹{remaining_limit:.2f}."
                )
                return

            self.balance -= amount
            self.total_withdrawn_today += amount
            self.record_transaction("Withdrawal", amount)

            print(f"Please collect your cash: ₹{amount:.2f}")
            print(f"Available balance: ₹{self.balance:.2f}")

        except ValueError as error:
            print("Error:", error)

    def check_balance(self):
        print(f"\nAccount holder: {self.account_holder}")
        print(f"Current balance: ₹{self.balance:.2f}")
        print(
            "Daily withdrawal limit remaining: ₹"
            f"{self.daily_withdrawal_limit - self.total_withdrawn_today:.2f}"
        )

    def transaction_summary(self):
        print("\n========== TRANSACTION SUMMARY ==========")

        if not self.transactions:
            print("No transactions have been recorded.")
        else:
            for index, transaction in enumerate(self.transactions, start=1):
                print(f"\nTransaction {index}")
                print(f"Type: {transaction['type']}")
                print(f"Amount: ₹{transaction['amount']:.2f}")
                print(f"Balance after transaction: ₹{transaction['balance']:.2f}")

                if transaction["note"]:
                    print(f"Note: {transaction['note']}")

        total_deposits = sum(
            (t["amount"] for t in self.transactions
             if t["type"] == "Deposit"),
            Decimal("0.00")
        )

        total_withdrawals = sum(
            (t["amount"] for t in self.transactions
             if t["type"] == "Withdrawal"),
            Decimal("0.00")
        )

        print("\n-------------- TOTALS --------------")
        print(f"Total deposits: ₹{total_deposits:.2f}")
        print(f"Total withdrawals: ₹{total_withdrawals:.2f}")
        print(f"Current balance: ₹{self.balance:.2f}")
        print("====================================")

    def run(self):
        while True:
            print("\n========== ATM MENU ==========")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Transaction Summary")
            print("5. Exit")
            print("==============================")

            choice = input("Select an option (1-5): ").strip()

            if choice == "1":
                self.deposit()
            elif choice == "2":
                self.withdraw()
            elif choice == "3":
                self.check_balance()
            elif choice == "4":
                self.transaction_summary()
            elif choice == "5":
                print("Thank you for using the ATM.")
                print(f"Final balance: ₹{self.balance:.2f}")
                break
            else:
                print("Invalid choice. Please select an option from 1 to 5.")


if __name__ == "__main__":
    atm = ATM(
        account_holder="Sample Customer",
        initial_balance=Decimal("10000.00"),
        daily_withdrawal_limit=Decimal("20000.00"),
        max_deposit=Decimal("50000.00"),
        max_withdrawal=Decimal("10000.00"),
    )

    atm.run()
