import time
from typing import List

from selenium.webdriver.remote.webelement import WebElement

from .loggedInPage import LoggedInPage
from .pageElements import PageElement, Locator


class ConnectorSettingsPage(LoggedInPage):

    DEFAULT_FEATURES = PageElement.by_css_selector("#aws-connector-default-features label")
    OPSCENTER_FEATURE_CHECKBOX = PageElement.by_css_selector("#aws-connector-feature-aws_ops_center label")
    SECURITY_HUB_FEATURE_CHECKBOX = PageElement.by_css_selector("#aws-connector-feature-aws_security_hub label")

    ENABLE_PROJECTS_BUTTON = PageElement.by_css_selector("#aws-connector-add-jira-project button")

    OPSCENTER_MAP_TO_PROJECT_MENU = PageElement.by_css_selector(".aws-connector-opscenter-projects")

    def disable_all_integrations(self):
        # When each checkbox is ticked the entire list of features is redrawn, invalidating any list, so we need to
        # do a new find_elements() call after each click
        for i in range(0, len(self.default_features_checkboxes())):
            feature = self.default_features_checkboxes()[i]
            if self.is_enabled(feature):
                feature.click()

    def enable_for_project(self, project_key: str) -> None:
        self.click(self.ENABLE_PROJECTS_BUTTON)
        time.sleep(1)
        self.click(PageElement.by_css_selector(f"#aws-connector-add-jira-project-{project_key} span"))

    def is_enabled(self, feature: WebElement) -> bool:
        checkbox = feature.find_element(*PageElement.by_css_selector('input'))
        return checkbox.is_selected()

    def default_features_checkboxes(self) -> List[WebElement]:
        return self.find_elements(self.DEFAULT_FEATURES)

    def enable_integration(self, locator: Locator, request_enabled: bool):
        feature = self.find_element(locator)
        is_enabled = self.is_enabled(feature)
        if is_enabled and not request_enabled:
            feature.click()  # disable
        elif not is_enabled and request_enabled:
            feature.click()  # enable

    def opscenter_integration(self, request_enabled: bool) -> None:
        self.enable_integration(self.OPSCENTER_FEATURE_CHECKBOX, request_enabled)

    def security_hub_integration(self, request_enabled: bool) -> None:
        self.enable_integration(self.SECURITY_HUB_FEATURE_CHECKBOX, request_enabled)

    def configure_opscenter(self, project_key: str) -> None:
        self.opscenter_integration(True)
        # FIXME open menu: what is the correct CSS selector to be able to open the menu
        # FIXME self.click(self.OPSCENTER_MAP_TO_PROJECT_MENU)
        # TODO find project from menu and click on it

    def configure_security_hub(self):
        self.security_hub_integration(True)
        # TODO
