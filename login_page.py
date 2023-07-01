"""Модуль для страницы входа.

Этот модуль содержит определение класса LoginPage, который предоставляет
методы для взаимодействия со страницей входа в банковском приложении.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_page import BasePage
from urls import LOGIN_PAGE_URL

from customer_page import CustomerPage


class LoginPage(BasePage):
    """Класс страницы входа.

    Предоставляет методы для открытия страницы и входа в систему как клиент.
    """

    def open_page(self) -> 'LoginPage':
        """Открывает страницу входа."""
        self.driver.get(LOGIN_PAGE_URL)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[ng-click="customer()"]'))
        )

        return self

    def click_customer_login(self) -> 'CustomerPage':
        """Вход в систему как клиент и переход на страницу клиента."""
        customer_login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[ng-click="customer()"]')
        customer_login_button.click()
        return CustomerPage(self.driver)
