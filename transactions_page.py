"""
Модуль, содержащий класс TransactionsPage, представляющий страницу транзакций в банковском приложении.
"""

from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base_page import BasePage


class TransactionsPage(BasePage):
    """Класс, представляющий страницу транзакций."""

    def open_transactions(self) -> 'TransactionsPage':
        """Открывает страницу транзакций."""
        transaction_button = self.driver.find_element(By.CSS_SELECTOR, 'button[ng-click="transactions()"]')
        transaction_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table.table-bordered.table-striped'))
        )
        return self

    def check_transactions(self) -> List[WebElement]:
        """Проверяет присутствие транзакций на странице."""
        transactions_elements = self.driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        return transactions_elements

    def get_transaction_data(self) -> List[List[str]]:
        """Получает данные транзакций со страницы."""
        transactions_elements = self.driver.find_elements(By.XPATH, '//tbody/tr')
        transactions = []
        for transaction_element in transactions_elements:
            date = transaction_element.find_element(By.XPATH, './td[1]').text
            amount = transaction_element.find_element(By.XPATH, './td[2]').text
            transaction_type = transaction_element.find_element(By.XPATH, './td[3]').text
            transactions.append([date, amount, transaction_type])
        return transactions
