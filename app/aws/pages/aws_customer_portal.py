from selenium_ui.jsm.pages.customer_pages import CustomerPortal
from selenium_ui.jsm.pages.customer_selectors import UrlManager, LoginPageLocators, TopPanelSelectors, \
    CustomerPortalsSelectors, CustomerPortalSelectors, RequestSelectors, RequestsSelectors, InsightSelectors


class AWSCustomerPortal(CustomerPortal):

    def __init__(self, driver, portal_id):
        CustomerPortal.__init__(self, driver, portal_id)

    def choose_aws_opsitem_request_type(self):
        request_types = self.get_elements(CustomerPortalSelectors.request_type)
        if len(request_types) > 1:
            request_type = next(filter(lambda rt: rt.text == 'AWS OpsItem', request_types))
        else:
            request_type = request_types[0]
        request_type.click()
        self.wait_until_visible(CustomerPortalSelectors.create_request_button)
