"""
╔══════════════════════════════════════════════════════╗
║           Simple Bank Account System                 ║
║         BankAccount & SavingsAccount Classes         ║
║                                                      ║
║         June/12 - Greg Tovar                         ║
╚══════════════════════════════════════════════════════╝
"""


# ─────────────────────────────────────────────
#  Domain Classes
# ─────────────────────────────────────────────

class BankAccount:
    #
    # A basic bank account with deposit and withdrawal support.
    #

    def __init__(self, owner: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.owner = owner
        self._balance = initial_balance
        self._history: list[str] = []

    @property
    def balance(self) -> float:
        return self._balance

#
# Deposit money into the account. 
# 
# Returns new balance.
#

    def deposit(self, amount: float) -> float:
        
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        self._history.append(f"  ➕  Deposited   ${amount:>10.2f}   →  Balance: ${self._balance:.2f}")
        return self._balance

#
#    Withdraw money from the account. Returns new balance.
#
#
    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds. Available: ${self._balance:.2f}, Requested: ${amount:.2f}"
            )
        self._balance -= amount
        self._history.append(f"  ➖  Withdrew    ${amount:>10.2f}   →  Balance: ${self._balance:.2f}")
        return self._balance

    def get_history(self) -> list[str]:
        return self._history.copy()

    def account_type(self) -> str:
        return "Checking Account"

    def __str__(self) -> str:
        return (
            f"[{self.account_type()}] Owner: {self.owner} | Balance: ${self._balance:.2f}"
        )



"""
A savings account that enforces a minimum balance requirement.

Withdrawals are allowed as long as the remaining balance stays
strictly above min_balance.

"""


class SavingsAccount(BankAccount):

    def __init__(self, owner: str, initial_balance: float = 0.0, min_balance: float = 0.0):
        super().__init__(owner, initial_balance)
        if min_balance < 0:
            raise ValueError("Minimum balance cannot be negative.")
        if initial_balance < min_balance:
            raise ValueError(
                f"Initial balance (${initial_balance:.2f}) cannot be below "
                f"minimum balance (${min_balance:.2f})."
            )
        self._min_balance = min_balance

    @property
    def min_balance(self) -> float:
        return self._min_balance

#
#  Withdraw money, enforcing the minimum balance rule.
#
#

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        projected = self._balance - amount
        if projected < self._min_balance:
            shortfall = self._min_balance - projected
            raise ValueError(
                f"Withdrawal denied. This would bring the balance to ${projected:.2f}, "
                f"which is below the minimum of ${self._min_balance:.2f}. "
                f"You can withdraw at most ${self._balance - self._min_balance:.2f} more."
            )
        self._balance -= amount
        self._history.append(
            f"  ➖  Withdrew    ${amount:>10.2f}   →  Balance: ${self._balance:.2f}  "
            f"(min: ${self._min_balance:.2f})"
        )
        return self._balance

    def account_type(self) -> str:
        return "Savings Account"

    def __str__(self) -> str:
        return (
            f"[{self.account_type()}] Owner: {self.owner} | "
            f"Balance: ${self._balance:.2f} | Min Balance: ${self._min_balance:.2f}"
        )


# ─────────────────────────────────────────────
#  Console UI Helpers
# ─────────────────────────────────────────────

BANNER = r"""
 ██████╗  █████╗ ███╗   ██╗██╗  ██╗
 ██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝
 ██████╔╝███████║██╔██╗ ██║█████╔╝
 ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗
 ██████╔╝██║  ██║██║ ╚████║██║  ██╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
       Banking System - Greg Tovar - 2026
"""

#
# The r makes it a raw string, which tells Python to treat 
# backslashes (\) as literal characters 
# rather than escape sequences.
#

WIDTH = 54


def divider(char="─"):
    print(char * WIDTH)


def header(title: str):
    print()
    divider("═")
    print(f"  {title}")
    divider("═")

#
#. These functions help for formtting console output
#
#

def info(msg: str):
    print(f"  ℹ️   {msg}")


def success(msg: str):
    print(f"  ✅  {msg}")


def error(msg: str):
    print(f"  ❌  {msg}")


def prompt_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(f"  {prompt}: ").strip())
            return value
        except ValueError:
            error("Please enter a valid number.")


def prompt_int(prompt: str, lo: int, hi: int) -> int:
    while True:
        try:
            value = int(input(f"  {prompt}: ").strip())
            if lo <= value <= hi:
                return value
            error(f"Please enter a number between {lo} and {hi}.")
        except ValueError:
            error("Please enter a whole number.")


# ─────────────────────────────────────────────
#  Account Creation Flow
# ─────────────────────────────────────────────

def create_account() -> BankAccount:
    header("Open a New Account")
    print("  What type of account would you like?\n")
    print("    1.  Checking Account  (no minimum balance)")
    print("    2.  Savings Account   (set a minimum balance)")
    print()
    choice = prompt_int("Choose [1-2]", 1, 2)
    print()

    owner = input("  Account holder name: ").strip() or "Customer"
    balance = prompt_float("Opening deposit ($)")

    if choice == 1:
        account = BankAccount(owner, balance)
        success(f"Checking account opened for {owner}!")
    else:
        min_bal = prompt_float("Minimum balance to maintain ($)")
        account = SavingsAccount(owner, balance, min_bal)
        success(f"Savings account opened for {owner}  (min: ${min_bal:.2f})!")

    return account


# ─────────────────────────────────────────────
#  Main Menu
# ─────────────────────────────────────────────

def show_account(account: BankAccount):
    header("Account Summary")
    print(f"  👤  Owner   : {account.owner}")
    print(f"  🏦  Type    : {account.account_type()}")
    print(f"  💰  Balance : ${account.balance:.2f}")
    if isinstance(account, SavingsAccount):
        print(f"  🔒  Min Bal : ${account.min_balance:.2f}")
        available = account.balance - account.min_balance
        print(f"  💸  Available to withdraw: ${available:.2f}")


def do_deposit(account: BankAccount):
    header("Deposit Funds")
    amount = prompt_float("Amount to deposit ($)")
    try:
        new_bal = account.deposit(amount)
        success(f"Deposited ${amount:.2f}. New balance: ${new_bal:.2f}")
    except ValueError as e:
        error(str(e))


def do_withdraw(account: BankAccount):
    header("Withdraw Funds")
    amount = prompt_float("Amount to withdraw ($)")
    try:
        new_bal = account.withdraw(amount)
        success(f"Withdrew ${amount:.2f}. New balance: ${new_bal:.2f}")
    except ValueError as e:
        error(str(e))


def show_history(account: BankAccount):
    header("Transaction History")
    history = account.get_history()
    if not history:
        info("No transactions yet.")
    else:
        for entry in history:
            print(entry)
    divider()


def main_menu(account: BankAccount):
    while True:
        header(f"Main Menu  ─  {account.owner}'s {account.account_type()}")
        print(f"  Balance: ${account.balance:.2f}\n")
        print("    1.  View account summary")
        print("    2.  Deposit money")
        print("    3.  Withdraw money")
        print("    4.  Transaction history")
        print("    5.  Switch / open new account")
        print("    6.  Exit")
        print()

        choice = prompt_int("Choose [1-6]", 1, 6)

        if choice == 1:
            show_account(account)
        elif choice == 2:
            do_deposit(account)
        elif choice == 3:
            do_withdraw(account)
        elif choice == 4:
            show_history(account)
        elif choice == 5:
            return True   # signal to open a new account
        else:
            header("Systems Stops! 2")
            info("Thanks for using the Banking System.")
            divider()
            print()
            return False  # signal to exit


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────

def run():
    print(BANNER)
    divider()
    print("  System Starts.\n")

    while True:
        try:
            account = create_account()
            keep_going = main_menu(account)
            if not keep_going:
                break
        except KeyboardInterrupt:
            print()
            header("Session interrupted")
            info("Goodbye!")
            divider()
            break
        except ValueError as e:
            error(f"Could not create account: {e}")
            print()



#
# Main Program, it just calls run()
#
#


if __name__ == "__main__":
    run()


#
# End of Main Program
#
#