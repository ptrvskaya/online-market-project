from main import Registration, Product, Cart

from dataclasses import asdict
from collections import defaultdict
import pytest


@pytest.fixture
def user():
    return Registration('John Doe', 'john.doe@example.com', '%05$ivQ!bo6Z', 10)


def test_user_str_representation(user):
    assert str(user) == 'User John Doe, balance - 10'


def test_set_valid_login(user):
    user.login = 'jane.doe@example.com'
    assert user.login == 'jane.doe@example.com'


@pytest.mark.parametrize("invalid_login", [
    'someinfo.com',
    'something@like@info.com',
    'some.info@com',
    'someinfo@com',
    '.some@info.com',
    '@someinfo.com',
    'someinfo@com.',
])
def test_set_invalid_login(user, invalid_login):
    with pytest.raises(ValueError):
        user.login = invalid_login



def test_as_dict(user):
    expected_dict = {
        'name': 'John Doe',
        'login': 'john.doe@example.com',
        'password': '%05$ivQ!bo6Z',
        'balance': 10
    }
    assert asdict(user) == expected_dict


def test_set_valid_password(user):
    user.password = '1wgJ@^wjA034'
    assert user.password == '1wgJ@^wjA034'

@pytest.mark.parametrize("invalid_password", [
    'pass',
    'password12345678',
    '1password18',
    'Password',
    'PASSWORD99',
    '123456',
    'пароль123',
    'password123'
])
def test_set_invalid(user, invalid_password):
    with pytest.raises(ValueError):
        user.password = invalid_password


def test_deposit(user):
    user.deposit(10000)
    assert user.balance == 10010
    

@pytest.fixture
def user_2():
    return Registration('John Doe', 'john.doe@example.com', '%05$ivQ!bo6Z')


@pytest.fixture
def product():
    return Product(name='T-shirt', price=20.0)


def test_product_str_representation(product):
    assert str(product) == 'Product: T-shirt, price: 20.0'


@pytest.fixture
def cart():
    return Cart(user)


def test_add(cart, product):
    cart.add(product)
    assert cart.goods == defaultdict(int, {product: 1})

    cart.add(product, number_of_products=3)
    assert cart.goods == defaultdict(int, {product: 4})


def test_remove(cart, product):
    cart.add(product, number_of_products=2)
    cart.remove(product)
    assert cart.goods == defaultdict(int, {product: 1})

    cart.remove(product, number_of_products=3)
    assert cart.goods == defaultdict(int, {})


def test_payment(user):
    user.deposit(5000)
    assert user.payment(4000) == True




