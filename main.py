from collections import defaultdict
from dataclasses import dataclass
import string
import re

LOGIN_RE_TEST = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

@dataclass
class Registration:

    name: str
    login: str
    password: str
    balance: float = 0.0

    def __str__(self) -> str:
        return f'User {self.name}, balance - {self.balance}'

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, value):
        if re.match(LOGIN_RE_TEST, value):
            self.__login = value
        else:
            raise ValueError("Enter your email address")


    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        if not 5 <= len(value) <= 14:
            raise ValueError('Password must be longer than 4 symbols and shorter than 15 symbols')
        if not Registration.includes_digit(value):
            raise ValueError('Password must contain at least one number')
        if not Registration.includes_all_register(value):
            raise ValueError('Password must contain at least one uppercase and lowercase character')
        if not Registration.includes_only_latin(value):
            raise ValueError('The password must contain only the Latin alphabet')
        if Registration.check_password_dictionary(value):
            raise ValueError('Your password is listed as the easiest')
        self.__password = value

    @staticmethod
    def includes_digit(value):
        for digit in string.digits:
            return bool(digit in value)

    @staticmethod
    def includes_all_register(value):
        result = ([any(map(lambda simbol: True if simbol in string.ascii_lowercase else False, value)), 
                    any(map(lambda simbol: True if simbol in string.ascii_uppercase else False, value))])
        return result

    @staticmethod
    def includes_only_latin(value):
        return value.isascii()

    @staticmethod
    def check_password_dictionary(value):
        with open('easy_passwords.txt', 'rt', encoding='utf-8') as file:
            file = file.readlines()
            file = [line.strip() for line in file]
            return bool(value in file)


    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        self.__balance = value

    def deposit(self, deposit_value: float):
        """
        This method is used for adding funds on the balance
        """
        self.__balance += deposit_value


    def payment(self, price: float):
        """
        This method checks if there are enough funds on the balance and if so, 
        subtracts the purchase amount from the balance to process the payment 
        """
        if self.__balance < price:
            print('\nNot enough funds on the balance')
            return False
        else:
            self.__balance -= price
            return True


@dataclass(frozen=True)
class Product:

    name: str
    price: float

    def __str__(self) -> str:
        return f'Product: {self.name}, price: {self.price}'


class Cart:
    
    def __init__(self, user: Registration) -> None:
        self.user = user
        self.goods = defaultdict(int) # key - product, value - amount
        self.__total = 0

    def add(self, product, number_of_products=1):
        """
        This method is used for adding products to cart
        """
        if not product in self.goods:
            self.goods[product] = self.goods.get(product, number_of_products)
        else:
            self.goods[product] += number_of_products
        self.__total += product.price * number_of_products
        print(f'{number_of_products} of {product.name} added to cart')

    def remove(self, product, number_of_products=1):
        """
        This method is used for removing products to cart.
        """
        if self.goods[product] > number_of_products:
            self.goods[product] -= number_of_products
            self.__total -= product.price * number_of_products
            print(f'{number_of_products} {product.name} removed from cart')
        else:
            self.__total -= self.goods[product] * product.price
            del self.goods[product]
            print(f'Product {product.name} removed from cart')

    def __str__(self) -> str:
        return f'Items in the cart for the amount {self.__total}'

    @property
    def total(self):
        return self.__total

    def order(self):
        """
        This method cheks if payment method returned True, 
        if so it will call the print_check method
        """
        if self.user.payment(self.total):
            print('\nOrder has been paid')
            self.print_check()
        else:
            print('Payment problem. Top up your account')

    def print_check(self):
        print('\n---Your check---')
        for key, value in sorted(self.goods.items(), key=lambda x: x[0].name):
            print(key.name, key.price, value, key.price * value)
        print(f'---Total: {self.total}---\n')
