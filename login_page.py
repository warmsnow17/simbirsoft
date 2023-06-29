from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_page import BasePage
from customer_page import CustomerPage
from urls import login_page_url


class LoginPage(BasePage):
    def open_page(self) -> 'LoginPage':
        self.driver.get(login_page_url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[ng-click="customer()"]'))
        )

        return self

    def click_customer_login(self) -> 'CustomerPage':
        customer_login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[ng-click="customer()"]')
        customer_login_button.click()
        return CustomerPage(self.driver)
