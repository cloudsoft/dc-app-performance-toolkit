from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jsm.pages.agent_pages import Login
from util.conf import JSM_SETTINGS

from aws import aws_modules_agents


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    # TODO: All variables below should come from the dataset. At least, they should be updated to match the ones from the instance under test
    issue_key = 'AWS-100'
    # Customfield ID for `AWS Region` on the `AWS OpsItem` issue/request type
    customfield_id = 'customfield_10811-val'

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action

    @print_timing("selenium_app_specific_user_login")
    def measure():
        def app_specific_user_login(username='admin', password='admin'):
            login_page = Login(webdriver)
            login_page.delete_all_cookies()
            login_page.go_to()
            login_page.set_credentials(username=username, password=password)
            if login_page.is_first_login():
                login_page.first_login_setup()
            if login_page.is_first_login_second_page():
                login_page.first_login_second_page_setup()
            login_page.wait_for_page_loaded()
        app_specific_user_login(username='admin', password='admin')
    measure()

    @print_timing("selenium_agent_aws_load_opsitems_project")
    def aws_load_opsitems_project():
        aws_modules_agents.load_opsitems_project(webdriver, datasets)
    aws_load_opsitems_project()

    @print_timing("selenium_agent_app_custom_action")
    def measure():

        @print_timing("selenium_agent_app_custom_action:view_request")
        def sub_measure():
            page.go_to_url(f"{JSM_SETTINGS.server_url}/browse/{issue_key}")
            # Wait for summary field visible
            page.wait_until_visible((By.ID, "summary-val"))
            # Wait for you app-specific UI element by ID selector
            page.wait_until_visible((By.ID, customfield_id))
        sub_measure()
    measure()
