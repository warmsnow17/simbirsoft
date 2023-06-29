import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from base_page import BasePage


class TransactionsPage(BasePage):
    def open_transactions(self) -> 'TransactionsPage':
        transaction_button = self.driver.find_element(By.CSS_SELECTOR, 'button[ng-click="transactions()"]')
        transaction_button.click()
        time.sleep(1)
        return self

    def check_transactions(self) -> List[WebElement]:
        transactions_elements = self.driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        return transactions_elements

    def get_transaction_data(self) -> List[List[str]]:
        transactions_elements = self.driver.find_elements(By.XPATH, '//tbody/tr')
        transactions = []
        for transaction_element in transactions_elements:
            date = transaction_element.find_element(By.XPATH, './td[1]').text
            amount = transaction_element.find_element(By.XPATH, './td[2]').text
            type = transaction_element.find_element(By.XPATH, './td[3]').text
            transactions.append([date, amount, type])
        return transactions

