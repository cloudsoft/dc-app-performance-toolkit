import time

from selenium_ui.jsm.pages.agent_pages import PopupManager
from .basePage import BasePage
from .pageElements import PageElement, Locator, PageFieldElement


class LoggedInPage(BasePage):

    __ADMIN_MENU = PageElement.by_css_selector("#admin_menu")
    __MANAGE_APPS_LINK = PageElement.by_css_selector("#admin_plugins_menu")
    __ADMIN_PROJECTS_MENU = PageElement.by_css_selector("#admin_project_menu")
    __TOOLBAR_CREATE_BUTTON = PageElement.by_css_selector("#create_link")
    __ISSUES_MENU = PageElement.by_css_selector("#find_link")
    __ISSUE_SEARCH_MENU = PageElement.by_css_selector("#issues_new_search_link_lnk")
    __ADMIN_ACCESS_PASSWORD = PageElement.by_css_selector("#login-form-authenticatePassword")
    __CONFIRM_PASSWORD_BUTTON = PageElement.by_css_selector("#login-form-submit")

    __admin_access_password = PageFieldElement(__ADMIN_ACCESS_PASSWORD)

    def click_manage_apps(self):
        self.click(self.__MANAGE_APPS_LINK)

    def click_admin_menu(self):
        self.click(self.__ADMIN_MENU)
        time.sleep(1)
        PopupManager(self.driver).dismiss_default_popup()

    def click_admin_projects_menu(self):
        self.click(self.__ADMIN_PROJECTS_MENU)

    def click_toolbar_create_button(self):
        self.click(self.__TOOLBAR_CREATE_BUTTON)

    def custom_field_locator(self, label: str) -> Locator:
        return PageElement.by_xpath(f"//label[text()='{label}']/../select")

    def click_issue_menu(self):
        self.click(self.__ISSUES_MENU)

    def click_issue_search_menu(self):
        self.click(self.__ISSUE_SEARCH_MENU)

    def confirm_password_if_required(self, password: str) -> None:
        time.sleep(1)
        if self.element_exists(self.__ADMIN_ACCESS_PASSWORD):
            self.__admin_access_password = password
            self.submit(self.__CONFIRM_PASSWORD_BUTTON)
