from selenium_ui.conftest import print_timing
from selenium_ui.jsm.pages.customer_pages import CustomerPortals

from .pages.aws_customer_portal import AWSCustomerPortal


def create_opsitem_request(webdriver, datasets):
    customer_portals = CustomerPortals(webdriver)
    # TODO: `portal_id` should come from the dataset. At least, it should be updated to match the portal ID on the instance under test
    customer_portal = AWSCustomerPortal(webdriver, portal_id=202)

    @print_timing("selenium_customer_aws_create_request")
    def measure():

        @print_timing("selenium_customer_aws_create_request:browse_all_portals")
        def sub_measure():
            customer_portals.browse_projects()
        sub_measure()

        @print_timing("selenium_customer_aws_create_request:view_portal")
        def sub_measure():
            customer_portal.go_to()
            customer_portal.wait_for_page_loaded()
        sub_measure()

        @print_timing("selenium_customer_aws_create_request:choose_aws_opsitem_request_type")
        def sub_measure():
            customer_portal.choose_aws_opsitem_request_type()
        sub_measure()

        @print_timing("selenium_customer_aws_create_request:create_and_submit_request")
        def sub_measure():
            customer_portal.create_and_submit_request()
        sub_measure()
    measure()
