import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from bank_operations import BankOperations
from base_page import BasePage


class CustomerPage(BasePage):
    def select_customer(self, customer_name: str) -> 'CustomerPage':
        select = Select(self.driver.find_element(By.ID, 'userSelect'))
        select.select_by_visible_text(customer_name)
        return self

    def click_login(self) -> 'BankOperations':
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        time.sleep(1)

        return BankOperations(self.driver)
