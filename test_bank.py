# pylint: disable=redefined-outer-name
"""Модуль для тестирования банковского приложения.

Этот модуль содержит тесты для различных функциональностей банковского приложения,
включая авторизацию, операции с депозитами и выводами, а также транзакции.
"""

import csv
import time
from typing import Generator, Tuple
import pytest
import allure # type: ignore
from allure_commons.types import AttachmentType # type: ignore
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
from login_page import LoginPage
from urls import SELENIUM_SERVER_URL, ACCOUNT_PAGE_URL, TRANSACTIONS_PAGE_URL
from utils import get_fibonacci_amount


@pytest.fixture
def setup() -> Generator[Tuple[Remote, LoginPage], None, None]:
    """Настройка тестового окружения."""
    options = Options()
    options.set_capability('browserName', 'chrome')

    driver = Remote(command_executor=SELENIUM_SERVER_URL, options=options)
    login_page = LoginPage(driver)
    login_page.open_page()

    yield driver, login_page

    driver.quit()


@allure.feature('Banking Application')
@allure.story('Login Test')
def test_login(setup: Tuple[Remote, LoginPage]) -> None:
    """Тестирование процесса авторизации."""
    driver, login_page = setup
    customer_page = login_page.click_customer_login()
    customer_page.select_customer('Harry Potter')
    customer_page.click_login()

    assert "XYZ Bank" in driver.title
    assert driver.current_url == ACCOUNT_PAGE_URL, \
        f'Ожидался {ACCOUNT_PAGE_URL}, но получили {driver.current_url}'


@allure.feature('Banking Application')
@allure.story('Deposit and Withdraw Test')
def test_deposit_withdraw(setup: Tuple[Remote, LoginPage]) -> None:
    """Тестирование операций депозита и вывода средств."""
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
    """Тестирование отображения транзакций."""
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
    assert driver.current_url == TRANSACTIONS_PAGE_URL, f'Ожидался {TRANSACTIONS_PAGE_URL}, ' \
                                                        f'но получили {driver.current_url}'

    transaction_data = transaction_page.get_transaction_data()

    with open('transactions.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(transaction_data)

    allure.attach.file('transactions.csv', name='transactions', attachment_type=AttachmentType.CSV)
