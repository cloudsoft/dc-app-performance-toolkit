from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.jira.pages.selectors import UrlManager


class ProjectPage(BasePage):
    page_loaded_selector =  (By.CLASS_NAME, 'sd-queue-table-container table td')

    def __init__(self, driver, project_key):
        BasePage.__init__(self, driver)
        url_manager = UrlManager(project_key=project_key)
        self.page_url = url_manager.project_summary_url()
