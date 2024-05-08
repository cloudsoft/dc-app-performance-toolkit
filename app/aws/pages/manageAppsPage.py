from .loggedInPage import LoggedInPage
from .pageElements import PageElement


class ManageAppsPage(LoggedInPage):

    AWS_ACCOUNT_LINK = PageElement.by_link_text("AWS accounts")
    CONNECTOR_SETTINGS_LINK = PageElement.by_link_text("Connector settings")

    def click_aws_accounts(self):
        self.click(self.AWS_ACCOUNT_LINK)

    def click_connector_settings(self) -> None:
        self.click(self.CONNECTOR_SETTINGS_LINK)
