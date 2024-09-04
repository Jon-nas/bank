import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class customer:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def make_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)

class individuals(customer):
    def __init__(self, name, birthdate, cpf, address):
        super().__init__(address)
        self.name = name
        self.birthdate = birthdate
        self.cpf = cpf

class account:
    def __init__(self, number, customer):
        self._balance = 0
        self._number = number
        self._angency = "0001"
        self._customer = customer
        self._history = history()

        @classmethod
        def new_account(cls, customer, number):
            return cls(number, customer)
        
        @property
        def balance(self):
            return self._balance
        
        @property
        def number(self):
            return self._number
        
        @property
        def agency(self):
            return self._agency
        
        @property
        def customer(self):
            return self._customer
        
        @property 
        def history(self):
            return self._history
        
        def draw(self, value):
            balance = self.balance
            exceeded_balance = value > balance

            if exceeded_balance:
                print("\n@@@ Operation failed! You don't have enough balance. @@@")

            elif value > 0:
                self._balance -= value
                print("\n@@@ Successful withdrawal! @@@")
                return True
            
            else:
                print("\n@@@ Operation failed! The value entered is invalid. @@@")
                
            return False
            
        def depositing(self, value):
            if value > 0:
                self._balance += value
                print("\n@@@ deposit successful! @@@")

            else:
                print("\n@@@ Operation failed! The value entered is invalid. @@@")
                return False
            
            return True
        
class current_account(account):
    def __init__(self, number, customer, limit = 500, withdrawal_limit = 3):
        super().__init__(number, customer)
        self._limit = limit
        self._withdrawal_limit = withdrawal_limit

    def draw(self, value):
        withdrawal_number = len(
            [transaction for transaction in self.history.transactions if transaction["type"] == withdrawal.__name__]
        )

        exceeded_limit = value > self.limit
        exceeded_withdrawal = withdrawal_number >= self._withdrawal_limit

        if exceeded_limit:
            print("\n@@@ Operation failed! The withdrawal amount exceeded the limit. @@@")

        elif exceeded_withdrawal:
            print("\n@@@ Operation failed! Maximum number of withdrawals exceeded. @@@")

        else:
            return super().draw(value)
        
        return False
    
    def __str__(self):
        return f"""\
            Agency:\t{self.agency}
            C/C:\t\t{self.number}
            Holder:\t{self.customer.name}
        """
    
class history:
    def __init__(self):
        self._transactions = []

    @property
    def translations(self):
        return self._transactions
    
    def add_transation(self, transaction):
        self._transactions.append(
            {
                "tipe": transaction.__class__.__name__,
                "value": transaction.value,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class transaction(ABC):
    @property
    @abstractmethod
    def value(self):
        pass

    @classmethod
    @abstractmethod
    def register(self, account):
        pass

class withdrawal(transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
    
    def register(self, account):
        transaction_sucess = account.draw(self.value)

        if transaction_sucess:
            account.history.add_transaction(self)

class deposit(transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
    
    def register(self, account):
        transaction_sucess = account.deposit(self.value)

        if transaction_sucess:
            account.history.add_transaction(self)

def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepositing
    [2]\tDraw
    [3]\tExtract
    [4]\tNew user
    [5]\tNew account
    [6]\tList accounts
    [0]\tExit
    => """
    return input(textwrap.dedent(menu))


def filter_customer(cpf, customers):
    filtered_customers = [customer for customer in customers if customer.cpf == cpf]
    return filtered_customers[0] if filtered_customers else None


def recover_account(customer):
    if not customer.accounts:
        print("\n@@@ No customer account! @@@")
        return
    
    # FIXME: No customer choice
    return customer.accounts[0]


def depositing(customers):
    cpf = input("Enter the customer's cpf: ")
    customer = filter_customer(cpf, customers)

    if not customer:
        print("\n@@@ Customer not found! @@@")
        return
    
    value = float(input("Inform the amount of the deposit: "))
    transaction = deposit(value)

    account = recover_account(customer)
    if not account:
        return
    
    customer.make_transaction(account, transaction)


def draw(customers):
    cpf = input("Enter the customer's cpf: ")
    customer = filter_customer(cpf, customers)

    if not customer:
        print("\n@@@ Customer not found! @@@")
        return
    
    value = float(input("Enter the amount of the withdrawal:: "))
    transaction = withdrawal(value)

    account = recover_account(customer)
    if not account:
        return
    
    customer.make_transaction(account, transaction)


def extract(customers):
    cpf = input("Enter the customer's cpf: ")
    customer = filter_customer(cpf, customers)

    if not customer:
        print("\n@@@ Customer not found! @@@")
        return
    
    account = recover_account(customer)
    if not account:
        return
    
    print("\n================ EXTRATO ================")
    transactions = account.history.transactions
    
    extract = ""
    if not transactions:
        extract = "No movements were made."
    else:
        for transaction in transactions:
            extract += f"\n{transaction['type']}:\n\tR${transaction['value']:.2f}"

    print(extract)
    print(f"\nBalance:\t\tR$ {account.balance:.2f}")
    print("==========================================")


def new_user(customers):
    cpf = input("Enter cpf (only numbers): ")
    customer = filter_customer(cpf, customers)

    if not customer:
        print("\n@@@ There is already a customer with this cpf. @@@")
        return
    
    name = input("Enter your full name: ")
    birthdate = input("Enter your date of birth (dd-mm-yyyy): ")
    address = input("Enter the address (street, number - neighborhood - city/state code): ")

    customer = individuals(name = name, birthdate = birthdate, cpf = cpf, address = address)

    customers.append(customer)

    print("\n @@@ User successfully created! @@@")


def new_account(account_number, customers, accounts):
    cpf = input("Enter the customer's cpf: ")
    customer = filter_customer(cpf, customers)

    if not customer:
        print("\n@@@ Customer not found. Account creation flow closed! @@@")
        return
    
    account = current_account.new_account(customer = customer, number = account_number)
    accounts.append(account)
    customer.accounts.append(account)

    print("\n@@@ Account successfully created! @@@")


def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def main():
    customers = []
    accounts = []
    
    while True:
        option = menu()

        if option == "1":
            depositing(customers)

        elif option == "2":
            draw(customers)

        elif option == "3":
            extract(customers)

        elif option == "4":
            new_user(customers)

        elif option == "5":
            accounts_number = len(accounts) + 1
            new_account(accounts_number, customers, accounts)

        elif option == "6":
            list_accounts(customers)

        elif option == "0":
            break

        else:
            print("Invalid operation, please select the desired operation again.")
            
main()