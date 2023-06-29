import time

from selenium.webdriver.common.by import By

from base_page import BasePage


class TransactionsPage(BasePage):
    def open_transactions(self):
        transaction_button = self.driver.find_element(By.CSS_SELECTOR, 'button[ng-click="transactions()"]')
        transaction_button.click()
        time.sleep(1)
        return self

    def check_transactions(self):
        transactions_elements = self.driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        return transactions_elements

    def get_transaction_data(self):
        transactions_elements = self.driver.find_elements(By.XPATH, '//tbody/tr')
        transactions = []
        for transaction_element in transactions_elements:
            date = transaction_element.find_element(By.XPATH, './td[1]').text
            amount = transaction_element.find_element(By.XPATH, './td[2]').text
            type = transaction_element.find_element(By.XPATH, './td[3]').text
            transactions.append([date, amount, type])
        return transactions

