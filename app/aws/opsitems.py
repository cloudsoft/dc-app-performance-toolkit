from util.project_paths import JSM_YML
from .conftest import print_timing
from .navigator import Navigator


def aws_opsitems(driver):

    navigator = Navigator(driver, JSM_YML)

    @print_timing("selenium_aws_admin_projects_page")
    def navigate_to_admin_projects_page():
        navigator.admin_projects_page()
    #navigate_to_admin_projects_page()

    @print_timing("selenium_aws_manage_apps_page")
    def navigate_to_manage_apps_page():
        navigator.manage_apps_page()
    #navigate_to_manage_apps_page()

    @print_timing("selenium_aws_account_list_page")
    def navigate_to_account_list_page():
        navigator.account_list_page()
    #navigate_to_account_list_page()

    @print_timing("selenium_aws_connector_settings_page")
    def navigate_to_connector_setting_page():
        navigator.connector_settings_page()
    #navigate_to_connector_setting_page()

    @print_timing("selenium_aws_opsitem_create_and_resolve")
    def opsitems_create_and_resolve():
        """create an ops item issue and resolve it"""
        #driver.navigate().to('/jira/secure/CreateIssue!default.jspa')
        issue_key = navigator.create_ops_item(
            project="AWS",
            summary="new ops item",
            description="ops item description",
            severity="4 - Low",
            category="Performance",
            region="eu-central-1")
        #navigator.resolve_issue(issue_key)
    opsitems_create_and_resolve()
