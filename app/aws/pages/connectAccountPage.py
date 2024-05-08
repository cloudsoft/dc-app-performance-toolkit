import time

from .basePage import BasePage
from .pageElements import PageFieldElement, PageElement


class AccountDetails:
    def __init__(self, alias: str, sync_key: str, sync_secret: str, end_key: str, end_secret: str):
        self.alias = alias
        self.sync_key = sync_key
        self.sync_secret = sync_secret
        self.end_key = end_key
        self.end_secret = end_secret


class ConnectAccountPage(BasePage):

    ACCOUNT_ALIAS = PageElement.by_name("accountAlias")
    SYNC_USER_KEY = PageElement.by_name("accessKeySyncUser")
    SYNC_USER_SECRET = PageElement.by_name("secretAccessKeySyncUser")
    END_USER_KEY = PageElement.by_name("accessKeyEndUser")
    END_USER_SECRET = PageElement.by_name("secretAccessKeyEndUser")
    ADD_AWS_REGION_BUTTON = PageElement.by_css_selector("#aws-add-region button")
    FRANKFURT_REGION = PageElement.by_css_selector("#aws-region-eu-central-1")
    CONNECT_BUTTON = PageElement.by_css_selector("#aws-connect-button button")

    account_alias = PageFieldElement(ACCOUNT_ALIAS)
    sync_user_key = PageFieldElement(SYNC_USER_KEY)
    sync_user_secret = PageFieldElement(SYNC_USER_SECRET)
    end_user_key = PageFieldElement(END_USER_KEY)
    end_user_secret = PageFieldElement(END_USER_SECRET)

    def click_add_region_button(self):
        self.click(self.ADD_AWS_REGION_BUTTON)

    def click_frankfurt_region(self):
        self.click(self.FRANKFURT_REGION)

    def click_connect_button(self):
        self.click(self.CONNECT_BUTTON)
        time.sleep(8)  # allows page reload and all toast notifications to clear

    def add_account_details(self, account_details: AccountDetails):
        self.account_alias = account_details.alias
        self.sync_user_key = account_details.sync_key
        self.sync_user_secret = account_details.sync_secret
        self.end_user_key = account_details.end_key
        self.end_user_secret = account_details.end_secret
