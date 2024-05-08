from .basePage import BasePage
from .pageElements import PageFieldElement, PageElement


class AccountDetailsPage(BasePage):

    ACCOUNT_ALIAS = PageElement.by_css_selector("#aws-account-alias h1")
    DELETE_BUTTON = PageElement.by_css_selector("#aws-account-delete button")
    CONFIRM_DELETE_BUTTON = PageElement.by_css_selector("footer button")
    SYNC_NOW_BUTTON = PageElement.by_css_selector("#aws-account-sync-now button")

    def click_delete(self):
        self.click(self.DELETE_BUTTON)

    def click_confirm_delete(self):
        self.click(self.CONFIRM_DELETE_BUTTON)

    def click_sync_now_button(self):
        self.click(self.SYNC_NOW_BUTTON)

    @property
    def alias(self):
        return PageElement(self.driver, self.ACCOUNT_ALIAS).text
