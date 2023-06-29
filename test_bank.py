import csv
import time
from typing import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from allure_commons.types import AttachmentType
import allure

from login_page import LoginPage
from urls import selenium_server_url, account_page_url, transactions_page_url
from utils import get_fibonacci_amount


@allure.feature('Banking Application')
class TestBank:

    @pytest.fixture
    def setup(self) -> Generator:
        options = Options()
        options.set_capability('browserName', 'chrome')

        self.driver = webdriver.Remote(command_executor=selenium_server_url, options=options)
        self.login_page = LoginPage(self.driver)
        self.login_page.open_page()
        time.sleep(3)
        yield
        self.driver.quit()

    @allure.story('Login Test')
    def test_login(self, setup: Generator) -> None:
        customer_page = self.login_page.click_customer_login()
        time.sleep(1)

        customer_page.select_customer('Harry Potter')
        time.sleep(1)

        bank_operations = customer_page.click_login()
        time.sleep(1)
        assert "XYZ Bank" in self.driver.title
        assert self.driver.current_url == account_page_url, \
            f'Ожидался {account_page_url}, но получили {self.driver.current_url}'

    @allure.story('Deposit and Withdraw Test')
    def test_deposit_withdraw(self, setup: Generator) -> None:
        customer_page = self.login_page.click_customer_login()
        time.sleep(1)

        customer_page.select_customer('Harry Potter')
        time.sleep(1)

        bank_operations = customer_page.click_login()
        time.sleep(1)

        amount = get_fibonacci_amount()

        bank_operations.make_deposit(amount)
        time.sleep(1)

        transaction_page = bank_operations.make_withdrawal(amount)
        time.sleep(1)

        assert "XYZ Bank" in self.driver.title
        assert bank_operations.check_balance() == 0, "Баланс после снятия средств не равен нулю"

    @allure.story('Transactions Test')
    def test_transactions(self, setup: Generator) -> None:
        customer_page = self.login_page.click_customer_login()
        time.sleep(1)

        customer_page.select_customer('Harry Potter')
        time.sleep(1)

        bank_operations = customer_page.click_login()
        time.sleep(1)

        amount = get_fibonacci_amount()
        bank_operations.make_deposit(amount)
        time.sleep(1)

        transaction_page = bank_operations.make_withdrawal(amount)
        time.sleep(1)

        transaction_page.open_transactions()
        time.sleep(1)

        transaction_elements = transaction_page.check_transactions()
        assert len(transaction_elements) >= 2, "Не найдено достаточное количество транзакций"
        assert self.driver.current_url == transactions_page_url, f'Ожидался {transactions_page_url}, ' \
                                                                 f'но получили {self.driver.current_url}'

        transaction_data = transaction_page.get_transaction_data()

        with open('transactions.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(transaction_data)

        allure.attach.file('transactions.csv', name='transactions', attachment_type=AttachmentType.CSV)
