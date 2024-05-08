from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Issue
from selenium_ui.jira.pages.selectors import IssueLocators
from util.api.jira_clients import JiraRestClient
from util.conf import JIRA_SETTINGS
from .pages.projectPage import ProjectPage


class Navigator:

    driver: WebDriver

    def __init__(self, driver):
        self.driver = driver

    def create_ops_item(self,
                        project: str,
                        summary: str,
                        description: str) -> None:
        client = JiraRestClient(JIRA_SETTINGS.server_url, JIRA_SETTINGS.admin_login, JIRA_SETTINGS.admin_password)
        rte_status = client.check_rte_status()

        @print_timing("load_aws_project")
        def load_aws_project():
            project_page = ProjectPage(self.driver, project_key=project)
            project_page.go_to()
            project_page.wait_for_page_loaded()
        load_aws_project()

        @print_timing("load_aws_create_issue_modal")
        def load_aws_create_issue_modal():
            issue_modal = Issue(self.driver)
            issue_modal.open_create_issue_modal()

            @print_timing("select_aws_opsitem_issue_type")
            def select_aws_opsitem_issue_type():
                issue_modal.get_element(IssueLocators.issue_type_field).click()
                issue_dropdown_elements: List[WebElement] = issue_modal.get_elements(IssueLocators.issue_type_dropdown_elements)
                if issue_dropdown_elements:
                    for element in issue_dropdown_elements:
                        cls = element.get_attribute('class')
                        if 'aui-list-item-li-aws-opsitem' in cls:
                            issue_modal.action_chains().move_to_element(
                                element).click(element).perform()
                issue_modal.wait_until_invisible(IssueLocators.issue_ready_to_save_spinner)
            select_aws_opsitem_issue_type()

            @print_timing("set_aws_opsitem_summary")
            def set_aws_opsitem_summary():
                issue_modal.wait_until_clickable(IssueLocators.issue_summary_field).send_keys(summary)
            set_aws_opsitem_summary()

            @print_timing("set_aws_opsitem_description")
            def set_aws_opsitem_description():
                if rte_status:
                    issue_modal.wait_until_available_to_switch(IssueLocators.issue_description_field_RTE)
                    issue_modal.get_element(IssueLocators.tinymce_description_field).send_keys(description)
                    issue_modal.return_to_parent_frame()
                else:
                    issue_modal.get_element(IssueLocators.issue_description_field).send_keys(description)
            set_aws_opsitem_description()

            @print_timing("submit_aws_opsitem")
            def submit_aws_opsitem():
                issue_modal.submit_issue()
            submit_aws_opsitem()

        load_aws_create_issue_modal()
