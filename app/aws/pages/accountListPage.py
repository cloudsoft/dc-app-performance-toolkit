import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .accountDetailsPage import AccountDetailsPage
from .basePage import BasePage
from .connectAccountPage import AccountDetails, ConnectAccountPage
from .pageElements import PageElement
from typing import List


class Account:

    def __init__(self, driver: WebDriver, manageLink: WebElement):
        self.driver = driver
        self.manageLink = manageLink

    def delete(self):
        self.manageLink.click()
        details_page = AccountDetailsPage(self.driver)
        details_page.click_delete()
        # time.sleep(2)
        details_page.click_confirm_delete()


class AccountListPage(BasePage):

    CONNECT_BUTTON = PageElement.by_css_selector(".aws-onboarding-container a")
    ACCOUNT_LIST = PageElement.by_css_selector('.aws-accounts-container section a')

    def has_connect_account_button(self):
        return "Connect your first account" in self.page_source

    def click_add_first_account(self):
        self.click(self.CONNECT_BUTTON)

    def account_list(self) -> List[WebElement]:
        try:
            return self.driver.find_elements(*self.ACCOUNT_LIST)
        except NoSuchElementException:
            # no accounts
            return []

    # the number of accounts listed on the page
    def count_accounts(self) -> int:
        return len(self.account_list())

    def accounts(self) -> List[Account]:
        return [Account(self.driver, account) for account in self.account_list()]

    def delete_all(self):
        time.sleep(1)
        [account.delete() for account in (self.accounts())]
        assert self.count_accounts() == 0

    def create_account(self, account_details: AccountDetails) -> AccountDetailsPage:
        connect_aws_account_page = ConnectAccountPage(self.driver)
        connect_aws_account_page.add_account_details(account_details)
        connect_aws_account_page.click_add_region_button()
        connect_aws_account_page.click_frankfurt_region()
        connect_aws_account_page.click_connect_button()
        return AccountDetailsPage(self.driver)

    def manage_account(self, index: int):
        account_list = self.account_list()
        assert len(account_list) > 0
        account = Account(self.driver, account_list[0])
        account.manageLink.click()
