import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from bank_operations import BankOperations


class CustomerPage:
    def __init__(self, driver):
        self.driver = driver

    def select_customer(self, customer_name):
        select = Select(self.driver.find_element(By.ID, 'userSelect'))
        select.select_by_visible_text(customer_name)
        return self

    def click_login(self):
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        time.sleep(1)

        return BankOperations(self.driver)