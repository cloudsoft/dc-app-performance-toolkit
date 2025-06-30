from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jsm.pages.agent_selectors import DashboardLocators
from selenium_ui.jsm.pages.customer_pages import Login, CustomerPortals
from selenium_ui.jsm.pages.customer_selectors import LoginPageLocators
from util.conf import JSM_SETTINGS

from aws import aws_modules_customers


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        custom_request_key = datasets['custom_issue_key']
        custom_service_desk_id = datasets['custom_service_desk_id']

    # TODO: All variables below should come from the dataset. At least, they should be updated to match the ones from the instance under test
    custom_request_key = 'AWS-421'
    custom_service_desk_id = '202'
    # Customfield ID for `AWS Region` on the `AWS OpsItem` issue/request type
    custom_field_id = 'content'

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action

    @print_timing("selenium_app_specific_user_login")
    def measure():
        def app_specific_user_login(username='admin', password='admin'):
            login = Login(webdriver)
            login.go_to()
            login.is_2sv()
            webdriver.app_version = login.get_app_version()
            # FIXME: not detecting that is logged in
            # if login.is_logged_in():
            print(">>> deleting all cookies")
            login.delete_all_cookies()
            print(">>> reload page")
            login.go_to()
            
            username = datasets['customers'][0][0]
            password = datasets['customers'][0][1]
            login.set_credentials(username, password)
            page = BasePage(webdriver)
            page.page_loaded_selector = (By.CSS_SELECTOR, "main#content")
            page.wait_for_page_loaded()
        app_specific_user_login(username='admin', password='admin')
    measure()

    @print_timing("selenium_customer_aws_create_opsitem_reques")
    def measure():
        aws_modules_customers.create_opsitem_request(webdriver, datasets)
    measure()
    print(">>> ok")

    # @print_timing("selenium_customer_app_custom_action")
    # def measure():
    #
    #     @print_timing("selenium_customer_app_custom_action:view_request")
    #     def sub_measure():
    #         # FIXME: ideally we should be opening the issue we just created
    #         url = f"{JSM_SETTINGS.server_url}/servicedesk/customer/portal/" \
    #                f"{custom_service_desk_id}/{custom_request_key}"
    #         print(">>> go to: ", url)
    #         page.go_to_url(url)
    #         # Wait for options element visible
    #         print(">>> waiting for page loaded")
    #         page.wait_until_visible((By.CLASS_NAME, 'cv-request-options'))
    #         # Wait for you app-specific UI element by ID selector
    #         # print(">>> waiting for custom field: ", custom_field_id)
    #         # page.wait_until_visible((By.XPATH, f"//dl[@data-test-id='{custom_field_id}']"))
    #         print(">>> custom field okay")
    #     sub_measure()
    # measure()
