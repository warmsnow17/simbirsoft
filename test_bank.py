import csv
import time
from typing import Generator, Tuple
from selenium.webdriver import Remote

from selenium.webdriver.chrome.options import Options

from login_page import LoginPage
from urls import selenium_server_url, account_page_url, transactions_page_url
from utils import get_fibonacci_amount
import pytest
import allure
from allure_commons.types import AttachmentType


@pytest.fixture
def setup() -> Generator[Tuple[Remote, LoginPage], None, None]:
    options = Options()
    options.set_capability('browserName', 'chrome')

    driver = Remote(command_executor=selenium_server_url, options=options)
    login_page = LoginPage(driver)
    login_page.open_page()

    yield driver, login_page

    driver.quit()


@allure.feature('Banking Application')
@allure.story('Login Test')
def test_login(setup: Tuple[Remote, LoginPage]) -> None:
    driver, login_page = setup
    customer_page = login_page.click_customer_login()
    customer_page.select_customer('Harry Potter')
    customer_page.click_login()

    assert "XYZ Bank" in driver.title
    assert driver.current_url == account_page_url, \
        f'Ожидался {account_page_url}, но получили {driver.current_url}'


@allure.feature('Banking Application')
@allure.story('Deposit and Withdraw Test')
def test_deposit_withdraw(setup: Tuple[Remote, LoginPage]) -> None:
    driver, login_page = setup
    customer_page = login_page.click_customer_login()
    customer_page.select_customer('Harry Potter')
    bank_operations = customer_page.click_login()
    amount = get_fibonacci_amount()
    bank_operations.make_deposit(amount)
    bank_operations.make_withdrawal(amount)

    assert "XYZ Bank" in driver.title
    assert bank_operations.check_balance() == 0, "Баланс после снятия средств не равен нулю"


@allure.feature('Banking Application')
@allure.story('Transactions Test')
def test_transactions(setup: Tuple[Remote, LoginPage]) -> None:
    driver, login_page = setup
    customer_page = login_page.click_customer_login()
    customer_page.select_customer('Harry Potter')
    bank_operations = customer_page.click_login()
    amount = get_fibonacci_amount()
    bank_operations.make_deposit(amount)
    transaction_page = bank_operations.make_withdrawal(amount)
    time.sleep(1)

    transaction_page.open_transactions()

    transaction_elements = transaction_page.check_transactions()
    assert len(transaction_elements) >= 2, "Не найдено достаточное количество транзакций"
    assert driver.current_url == transactions_page_url, f'Ожидался {transactions_page_url}, ' \
                                                        f'но получили {driver.current_url}'

    transaction_data = transaction_page.get_transaction_data()

    with open('transactions.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(transaction_data)

    allure.attach.file('transactions.csv', name='transactions', attachment_type=AttachmentType.CSV)
