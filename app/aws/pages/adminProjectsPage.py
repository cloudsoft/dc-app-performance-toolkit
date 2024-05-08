import time
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from .loggedInPage import LoggedInPage
from .pageElements import PageElement, PageFieldElement


class ProjectNotFoundError(AssertionError):
    pass


class NonUniqueProjectPrefixError(AssertionError):
    pass


class AdminProjectsPage(LoggedInPage):

    SEARCH_FIELD = PageElement.by_css_selector("#project-filter-text")
    PROJECT_LIST = PageElement.by_css_selector('.p-list tr .cell-type-name a')
    PROJECT_LINK_FOR_ROW = PageElement.by_css_selector(".cell-type-name a")
    CREATE_PROJECT_BUTTON = PageElement.by_css_selector(".add-project-trigger")

    CREATE_PROJECT_NEXT_BUTTON = PageElement.by_css_selector(".create-project-dialog-create-button")
    CREATE_PROJECT_NAME_FIELD = PageElement.by_css_selector("#add-project-form #name")
    CREATE_PROJECT_KEY_FIELD = PageElement.by_css_selector("#add-project-form #key")
    CREATE_PROJECT_SUBMIT_BUTTON = PageElement.by_css_selector(".add-project-dialog-create-button")

    search_field = PageFieldElement(SEARCH_FIELD)
    create_project_name = PageFieldElement(CREATE_PROJECT_NAME_FIELD)
    create_project_key = PageFieldElement(CREATE_PROJECT_KEY_FIELD)

    def find_and_click_project(self, project_key: str):
        # FIXME check there are any projects
        self.search_field = project_key
        time.sleep(1)
        projects_count = self.count_projects()
        if projects_count < 1:
            raise ProjectNotFoundError("Project not found: " + project_key)
        if projects_count > 1:
            raise NonUniqueProjectPrefixError("Duplicate projects found: " + project_key)
        project_link = self.project_list()[0]
        project_link.click()

    def count_projects(self):
        return len(self.project_list())

    def project_list(self) -> List[WebElement]:
        try:
            return self.driver.find_elements(*self.PROJECT_LIST)
        except NoSuchElementException:
            # no accounts
            return []

    def click_create_project_button(self):
        self.click(self.CREATE_PROJECT_BUTTON)

    def click_create_project_next_button(self):
        self.click(self.CREATE_PROJECT_NEXT_BUTTON)

    def click_create_project_submit_button(self):
        self.click(self.CREATE_PROJECT_SUBMIT_BUTTON)
        time.sleep(10)
