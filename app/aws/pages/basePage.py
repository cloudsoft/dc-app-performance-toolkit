from selenium.webdriver.chrome.webdriver import WebDriver

from .pageElements import PageElement, Locator


class BasePage:

    driver: WebDriver

    def __init__(self, driver):
        self.driver = driver

    @property
    def page_source(self) -> str:
        return self.driver.page_source

    def page_element(self, locator: Locator) -> PageElement:
        return PageElement(self.driver, locator)

    def element_exists(self, locator: Locator) -> bool:
        return self.page_element(locator).exists()

    def find_element(self, locator: Locator):
        return self.page_element(locator).find_element()

    def find_elements(self, locator: Locator):
        return self.page_element(locator).find_elements()

    def click(self, locator: Locator) -> None:
        self.page_element(locator).click()

    def submit(self, locator: Locator) -> None:
        """submit a form element

        locator: must be a form element
        """
        self.find_element(locator).submit()
