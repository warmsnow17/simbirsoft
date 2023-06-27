import csv
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from allure_commons.types import AttachmentType
import allure


from login_page import LoginPage


@allure.feature('Banking Application')
class TestBank:


    @pytest.fixture
    def setup(self):
        options = Options()
        options.set_capability('browserName', 'chrome')
        options.add_argument('--disable-blink-features=AutomationControlled')


        self.driver = webdriver.Remote(command_executor='http://192.168.0.13:4444', options=options)
        self.login_page = LoginPage(self.driver)
        self.login_page.open()
        time.sleep(3)

        yield
        self.driver.quit()


    @allure.story('Login Test')
    def test_login(self, setup):
        customer_page = self.login_page.click_customer_login()
        time.sleep(1)

        customer_page.select_customer('Harry Potter')
        time.sleep(1)

        bank_operations = customer_page.click_login()
        time.sleep(1)
        assert "XYZ Bank" in self.driver.title

    @allure.story('Deposit and Withdraw Test')
    def test_deposit_withdraw(self, setup):
        customer_page = self.login_page.click_customer_login()
        time.sleep(1)

        customer_page.select_customer('Harry Potter')
        time.sleep(1)

        bank_operations = customer_page.click_login()
        time.sleep(1)

        amount = bank_operations.get_fibonacci_amount()

        bank_operations.make_deposit(amount)
        time.sleep(1)

        transaction_page = bank_operations.make_withdrawal(amount)
        time.sleep(1)

        assert "XYZ Bank" in self.driver.title
        assert bank_operations.check_balance() == 0, "Баланс после снятия средств не равен нулю"

    @allure.story('Transactions Test')
    def test_transactions(self, setup):
        customer_page = self.login_page.click_customer_login()
        time.sleep(1)

        customer_page.select_customer('Harry Potter')
        time.sleep(1)

        bank_operations = customer_page.click_login()
        time.sleep(1)

        amount = bank_operations.get_fibonacci_amount()
        bank_operations.make_deposit(amount)
        time.sleep(1)

        transaction_page = bank_operations.make_withdrawal(amount)
        time.sleep(1)

        transaction_page.open_transactions()
        time.sleep(1)

        transaction_elements = transaction_page.check_transactions()
        assert len(transaction_elements) >= 2, "Не найдено достаточное количество транзакций"

        transaction_data = transaction_page.get_transaction_data()

        with open('transactions.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(transaction_data)

        allure.attach.file('transactions.csv', attachment_type=AttachmentType.CSV)

