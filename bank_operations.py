import datetime
import time

from selenium.webdriver.common.by import By

from base_page import BasePage
from transactions_page import TransactionsPage


class BankOperations(BasePage):

    def make_deposit(self, amount: int) -> 'BankOperations':
        deposit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[ng-click="deposit()"]')
        deposit_button.click()
        time.sleep(1)

        deposit_input = self.driver.find_element(By.CSS_SELECTOR, 'input[ng-model="amount"]')
        deposit_input.send_keys(str(amount))

        confirm_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        confirm_button.click()
        time.sleep(1)
        return self

    def make_withdrawal(self, amount: int) -> 'TransactionsPage':
        withdrawal_button = self.driver.find_element(By.CSS_SELECTOR, 'button[ng-click="withdrawl()"]')
        withdrawal_button.click()
        time.sleep(1)

        withdrawal_input = self.driver.find_element(By.CSS_SELECTOR, 'input[ng-model="amount"]')
        withdrawal_input.send_keys(str(amount))

        confirm_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        confirm_button.click()
        time.sleep(1)
        return TransactionsPage(self.driver)

    def check_balance(self) -> int:
        balance_element = self.driver.find_element(By.XPATH, '//div[@ng-hide="noAccount"]/strong[2]')
        balance = int(balance_element.text)
        return balance
