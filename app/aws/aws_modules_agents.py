from selenium_ui.conftest import print_timing
from selenium_ui.jsm.pages.agent_pages import Login, PopupManager, Logout, BrowseProjects, BrowseCustomers, \
    ViewCustomerRequest, ViewQueue, Report, InsightLogin, InsightNewSchema, InsightNewObject, InsightDeleteSchema, \
    InsightViewQueue, ViewIssueWithObject, InsightSearchByIql
from selenium_ui.jsm.pages.agent_selectors import LoginPageLocators, PopupLocators, DashboardLocators, LogoutLocators, \
    BrowseProjectsLocators, BrowseCustomersLocators, ViewCustomerRequestLocators, UrlManager, ViewReportsLocators, \
    ViewQueueLocators, InsightViewQueueLocators, InsightViewIssue, InsightDeleteSchemaLocators, \
    InsightNewSchemaLocators, InsightNewObjectLocators, InsightSearchObjectIql

def load_opsitems_project(webdriver, datasets):
    @print_timing("load_opsitems_project")
    def measure():
        # TODO: `project_key` and `queue_id` should come from the dataset. At least, they should be updated to match the ones from the instance under test
        view_queue = ViewQueue(webdriver, project_key="AWS", queue_id='1102')
        view_queue.go_to()
        view_queue.wait_for_page_loaded()

    measure()
    PopupManager(webdriver).dismiss_default_popup()
