"""Модуль для страницы клиента.

Этот модуль содержит определение класса CustomerPage, который предоставляет
методы для взаимодействия со страницей клиента в банковском приложении.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_page import BasePage

from bank_operations import BankOperations


class CustomerPage(BasePage):
    """Класс страницы клиента.

    Предоставляет методы для выбора клиента и входа в систему.
    """

    def select_customer(self, customer_name: str) -> 'CustomerPage':
        """Выберите клиента по имени."""
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'label'), 'Your Name :')
        )
        select = Select(self.driver.find_element(By.ID, 'userSelect'))
        select.select_by_visible_text(customer_name)
        return self

    def click_login(self) -> 'BankOperations':
        """Войдите в систему и перейдите на страницу банковских операций."""
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[ng-click="deposit()"]'))
        )

        return BankOperations(self.driver)
