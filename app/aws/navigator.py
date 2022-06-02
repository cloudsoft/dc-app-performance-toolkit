import json
import time
from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Issue, Project
from selenium_ui.jira.pages.selectors import IssueLocators
from selenium_ui.jsm.pages.agent_pages import Login
from util.conf import BaseAppSettings
from .pages.accountDetailsPage import AccountDetailsPage
from .pages.accountListPage import AccountListPage
from .pages.adminProjectsPage import AdminProjectsPage, ProjectNotFoundError
from .pages.connectAccountPage import AccountDetails
from .pages.connectorSettingsPage import ConnectorSettingsPage
from .pages.createIssueFirstPage import CreateIssueFirstPage
from .pages.loggedInPage import LoggedInPage
from .pages.manageAppsPage import ManageAppsPage
from .pages.projectPage import ProjectPage
from .pages.viewIssuePage import ViewIssuePage


class Navigator:

    driver: WebDriver
    logged_in: bool
    has_account: bool
    last_page: str

    account_details = AccountDetails(
        alias = "cloudsoftqa",
        sync_key = "",  # os.environ['AWS_QA_SYNC_KEY'],
        sync_secret = "",  # os.environ['AWS_QA_SYNC_SECRET'],
        end_key = "",  # os.environ['AWS_QA_END_KEY'],
        end_secret = "",  # os.environ['AWS_QA_END_SECRET']
    )

    def __init__(self, driver, yaml_file):
        self.driver = driver
        self.logged_in = False
        self.has_account = False
        self.last_page = 'unknown'
        self.settings = BaseAppSettings(config_yml=yaml_file)
        self.site_url = self.settings.server_url
        self.site_user = self.settings.admin_login
        self.site_password = self.settings.admin_password

    def login(self) -> LoggedInPage:
        if not self.logged_in:
            login_page = Login(self.driver)
            login_page.go_to()
            self.driver.node_id = login_page.get_node_id()
            login_page.set_credentials(username=self.site_user, password=self.site_password)
            if login_page.is_first_login():
                login_page.first_login_setup()
            if login_page.is_first_login_second_page():
                login_page.first_login_second_page_setup()
            login_page.wait_for_page_loaded()
            self.logged_in = True
        return LoggedInPage(self.driver)

    def manage_apps_page(self) -> ManageAppsPage:
        if not self.last_page == 'manage_apps':
            page = self.login()
            page.click_admin_menu()
            page.click_manage_apps()
            page.confirm_password_if_required(self.site_password)
            self.last_page = 'manage_apps'
        return ManageAppsPage(self.driver)

    def account_list_page(self) -> AccountListPage:
        if not self.last_page == 'account_list':
            self.manage_apps_page().click_aws_accounts()
            self.last_page = 'account_list'
        return AccountListPage(self.driver)

    def account_details_page(self, index: int) -> AccountDetailsPage:
        if not self.last_page == 'account_details_' + str(index):
            self.account_list_page().manage_account(index)
            self.last_page = 'account_details_' + str(index)
        return AccountDetailsPage(self.driver)

    def connector_settings_page(self) -> ConnectorSettingsPage:
        if not self.last_page == 'connector_settings':
            self.manage_apps_page().click_connector_settings()
            self.last_page = 'connector_settings'
        return ConnectorSettingsPage(self.driver)

    def connect_account(self) -> AccountDetailsPage:
        if not self.last_page == 'account_details':
            account_list_page = self.account_list_page()
            account_list_page.delete_all()
            account_list_page.click_add_first_account()
            account_details_page = account_list_page.create_account(self.account_details)
            self.has_account = True
            self.last_page = 'account_details'
            return account_details_page
        return AccountDetailsPage(self.driver)

    def connect_account_and_sync(self) -> AccountDetailsPage:
        account_details_page = self.connect_account()
        account_details_page.click_sync_now_button()
        return account_details_page

    def sync_connected_account(self, index: int) -> AccountDetailsPage:
        account_details_page = self.account_details_page(index)
        account_details_page.click_sync_now_button()
        return account_details_page

    def create_project(self, project_name: str, project_key: str) -> ProjectPage:
        page = self.admin_projects_page()
        page.click_create_project_button()
        page.click_create_project_next_button()
        page.create_project_name = project_name + Keys.TAB
        page.create_project_key = project_key + Keys.TAB
        page.click_create_project_submit_button()
        self.last_page = "project_page_" + project_key
        return self.project_page(project_key)

    def configure_connector(self, project_key: str):
        connector_settings_page = self.connector_settings_page()
        connector_settings_page.disable_all_integrations()
        connector_settings_page.enable_for_project(project_key)
        connector_settings_page.configure_opscenter(project_key)
        connector_settings_page.configure_security_hub()
        time.sleep(100)
        # TODO SAVE

    def admin_projects_page(self) -> AdminProjectsPage:
        print("Admin Project Page - Last Page: " + self.last_page)
        # secure/project/BrowseProjects.jspa?s=view_projects
        #if not self.last_page == "admin_projects":
        page = self.login()
        page.click_admin_menu()
        page.click_admin_projects_menu()
        self.last_page = "admin_projects"
        return AdminProjectsPage(self.driver)

    def create_issue_page(self):
        if not self.last_page == "create_issue":
            self.admin_projects_page().click_toolbar_create_button()
            self.last_page = "create_issue"
        return CreateIssueFirstPage(self.driver)

    def project_page(self, project_key: str) -> ProjectPage:
        if not self.last_page == "project_page_" + project_key:
            page = self.admin_projects_page()
            page.find_and_click_project(project_key)
            self.last_page = "project_page_" + project_key
        return ProjectPage(self.driver)

    def delete_project_if_exists(self, project_key) -> AdminProjectsPage:
        try:
            project_page = self.project_page(project_key)
            project_page.delete_project()
            self.last_page = "admin_projects"
            return self.admin_projects_page()
        except ProjectNotFoundError:
            return self.admin_projects_page()

    def create_ops_item(self,
                        project: str,
                        summary: str,
                        description: str,
                        severity: str,
                        category: str,
                        region: str) -> str:
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
                        print(f'cls: {cls}')
                        if 'aui-list-item-li-aws-opsitem' in cls:
                            issue_modal.action_chains().move_to_element(element).click(element).perform()
                issue_modal.wait_until_invisible(IssueLocators.issue_ready_to_save_spinner)
            select_aws_opsitem_issue_type()

            @print_timing("set aws_opsitem_summary")
            def set_aws_opsitem_summary():
                issue_modal.wait_until_clickable(IssueLocators.issue_summary_field).send_keys(summary)
            set_aws_opsitem_summary()

            time.sleep(20)

        load_aws_create_issue_modal()

        # page2.set_summary(summary)
        # page2.set_description(description)
        # page2.set_severity(severity)
        # page2.set_category(category)
        # page2.set_region(region)
        # page2.create()
        # issue_page = ViewIssuePage(self.driver)
        # issue_key = issue_page.issue_key
        # self.last_page = "issue_page_" + issue_key
        # return issue_key

    def resolve_issue(self, issue_key: str) -> None:
        issue_page = self.issue_page(issue_key)
        issue_page.resolve()

    def issue_page(self, issue_key: str):
        if not self.last_page == "issue_page_" + issue_key:
            self.get("browse/" + issue_key)
            self.last_page = "issue_page_" + issue_key
        return ViewIssuePage(self.driver)

    def get(self, path: str):
        url = self.site_url + path
        self.driver.get(url)

    def find_open_ops_item(self, project_key: str) -> str:
        issue_key = self.search_issue(project_key=project_key, issue_type="AWS OpsItem", status="Open")
        return issue_key

    def in_progress_issue(self, issue_key: str) -> None:
        issue_page = self.issue_page(issue_key)
        issue_page.in_progress()

    def search_issue(self, project_key: str, issue_type: str, status: str) -> str:
        page = self.issue_search_page()
        page.filter_project(project_key)
        page.filter_type(issue_type)
        page.filter_status(status)
        # TODO - does this need a delay?
        return page.issue_key

    def issue_search_page(self) -> ViewIssuePage:
        if not self.last_page.startswith("issue_search"):
            page = self.login()
            page.click_issue_menu()
            page.click_issue_search_menu()
            self.last_page = "issue_search"
        return ViewIssuePage(self.driver)


