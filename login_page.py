from selenium.webdriver.common.by import By

from customer_page import CustomerPage


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get('https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login')
        return self

    def click_customer_login(self):
        customer_login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[ng-click="customer()"]')
        customer_login_button.click()
        return CustomerPage(self.driver)
