from collections import defaultdict
from dataclasses import dataclass
import string
import re


@dataclass
class Registration:
    name: str
    login: str
    password: str
    balance: float = 0.0


    def __str__(self) -> str:
        return f'Пользователь {self.name}, баланс - {self.balance}'

    @property
    def login(self):
        return self.__login


    @login.setter
    def login(self, value):
        login_re_test = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(login_re_test, value):
            self.__login = value
        else:
            raise ValueError("Введите адрес почты")


    @property
    def password(self):
        return self.__password


    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypeError("Пароль должен быть строкой")
        if not 5 <= len(value) <= 14:
            raise ValueError('Пароль должен быть длиннее 4 и меньше 15 символов')
        if not Registration.is_include_digit(value):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not Registration.is_include_all_register(value):
            raise ValueError('Пароль должен содержать хотя бы один символ верхнего и нижнего регистра')
        if not Registration.is_include_only_latin(value):
            raise ValueError('Пароль должен содержать только латинский алфавит')
        if Registration.check_password_dictionary(value):
            raise ValueError('Ваш пароль содержится в списке самых легких')
        self.__password = value


    @staticmethod
    def is_include_digit(value):
        for digit in string.digits:
            return bool(digit in value)


    @staticmethod
    def is_include_all_register(value):
        result = all([any(map(lambda simbol: True if simbol in string.ascii_lowercase else False, value)), any(map(lambda simbol: True if simbol in string.ascii_uppercase else False, value))])
        return result


    @staticmethod
    def is_include_only_latin(value):
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


    def deposit(self, deposit_value):
        self.__balance += deposit_value


    def payment(self, price):
        if self.__balance < price:
            print('\nНе хватает средств на балансе')
            return False
        else:
            self.__balance -= price
            return True



@dataclass(frozen=True)
class Product:

    name: str
    price: float


    def __str__(self) -> str:
        return f'Товар: {self.name}, цена: {self.price}'





class Cart:
    
    def __init__(self, user) -> None:
        self.user = user
        self.goods = defaultdict(int) # ключ словаря - товар, значение - количество
        self.__total = 0


    def add(self, product, number_of_products=1):
        if not product in self.goods:
            self.goods[product] = self.goods.get(product, number_of_products)
        else:
            self.goods[product] += number_of_products
        self.__total += product.price * number_of_products
        return f'{number_of_products} штук товара {product.name} добавлено в корзину'


    def remove(self, product, number_of_products=1):
        if self.goods[product] > number_of_products:
            self.goods[product] -= number_of_products
            self.__total -= product.price * number_of_products
            print(f'{number_of_products} {product.name} удалено из корзины')
        else:
            self.__total -= self.goods[product] * product.price
            del self.goods[product]
            print(f'Товар {product.name} удален из корзины')


    def __str__(self) -> str:
        return f'Товаров в корзине на сумму {self.__total}'


    @property
    def total(self):
        return self.__total


    def order(self):
        if self.user.payment(self.total):
            print('\nЗаказ оплачен')
            self.print_check()
        else:
            print('Проблема с оплатой. Пополните счет')


    def print_check(self):
        print('\n---Your check---')
        for key, value in sorted(self.goods.items(), key=lambda x: x[0].name):
            print(key.name, key.price, value, key.price * value)
        print(f'---Total: {self.total}---\n')




