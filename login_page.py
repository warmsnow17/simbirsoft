from selenium.webdriver.common.by import By

from base_page import BasePage
from customer_page import CustomerPage
from urls import login_page_url


class LoginPage(BasePage):
    def open_page(self):
        self.driver.get(login_page_url)
        return self

    def click_customer_login(self):
        customer_login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[ng-click="customer()"]')
        customer_login_button.click()
        return CustomerPage(self.driver)
