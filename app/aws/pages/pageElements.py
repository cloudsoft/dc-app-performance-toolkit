from typing import List, NewType

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


Locator = NewType('Locator', (str, str))


class PageElement:

    __timeout_seconds: int = 20
    driver: WebDriver
    locator: Locator

    def __init__(self, driver: WebDriver, locator: Locator):
        self.driver = driver
        self.locator = locator

    @staticmethod
    def by_css_selector(css_selector: str) -> Locator:
        return By.CSS_SELECTOR, css_selector

    @staticmethod
    def by_id(id: str) -> Locator:
        return By.ID, id

    @staticmethod
    def by_button_text(text: str) -> Locator:
        return By.XPATH, text

    @staticmethod
    def by_name(name: str) -> Locator:
        return By.NAME, name

    @staticmethod
    def by_link_text(link_text: str) -> Locator:
        return By.LINK_TEXT, link_text

    @staticmethod
    def by_partial_link_text(partial_link_text: str) -> Locator:
        return By.PARTIAL_LINK_TEXT, partial_link_text

    @staticmethod
    def by_xpath(xpath: str) -> Locator:
        return By.XPATH, xpath

    def find_element(self) -> WebElement:
        self.wait_for_element()
        element = self.driver.find_element(*self.locator)
        return element

    def click(self) -> None:
        self.find_element().click()

    def count(self) -> int:
        return len(self.driver.find_elements(*self.locator))

    def find_elements(self) -> List[WebElement]:
        self.wait_for_element()
        elements = self.driver.find_elements(*self.locator)
        return elements

    def wait_for_element(self) -> None:
        WebDriverWait(self.driver, self.__timeout_seconds).until(
            lambda driver: driver.find_element(*self.locator))

    @property
    def text(self):
        return self.find_element().text

    def exists(self):
        # doesn't wait for the element
        try:
            element = self.driver.find_element(*self.locator)
            return element is not None
        except NoSuchElementException:
            return False


class PageFieldElement:

    def __init__(self, locator):
        self.locator = locator

    def __set__(self, instance, value) -> None:
        element = PageElement(instance.driver, self.locator).find_element()
        element.clear()
        element.send_keys(value)

    def __get__(self, instance, owner) -> str:
        element = PageElement(instance.driver, self.locator).find_element()
        return element.get_attribute("value")
