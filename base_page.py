"""Модуль для базовой страницы.

Этот модуль содержит определение класса BasePage, который является
родительским классом для всех классов страниц в этом проекте.
"""

from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    """Базовый класс для всех страниц проекта.

    Каждый класс страницы должен наследовать этот класс и может
    переопределить его методы для специфичных для страницы действий.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_current_url(self):
        """Метод для получения текущего URL.

        Этот метод возвращает текущий URL, открытый в драйвере.
        """
        return self.driver.current_url
