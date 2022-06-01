from .createIssueSecondPage import CreateIssueSecondPage
from .pageElements import Locator, PageElement


class CreateOpsItemIssuePage(CreateIssueSecondPage):

    severity_label: Locator
    severity_select: Locator
    category_select: Locator
    region_select: Locator

    def __init__(self, driver):
        super().__init__(driver)
        self.severity_select = self.custom_field_locator("Severity")
        self.category_select = self.custom_field_locator("Category")
        self.region_select = self.custom_field_locator("Region")


    def set_project(self, project_key: str):
        self.click(PageElement.by_css_selector("#project-single-select > span"))
        if f"({project_key})" not in self.__project:
            self.click(PageElement.by_partial_link_text(f"({project_key})"))
        else:
            self.click(PageElement.by_css_selector("#project-single-select > span"))

    def set_issue_type(self, issue_type: str):
        self.click(PageElement.by_css_selector("#issuetype-single-select > span"))
        if issue_type not in self.__issue_type:
            self.click(PageElement.by_link_text(issue_type))
        else:
            self.click(PageElement.by_css_selector("#issuetype-single-select > span"))

    def set_severity(self, severity: str) -> None:
        self.select_option(severity, self.severity_select)

    def set_category(self, category: str) -> None:
        self.select_option(category, self.category_select)

    def set_region(self, region: str) -> None:
        self.select_option(region, self.region_select)

    def select_option(self, value: str, select_locator: Locator) -> None:
        select = self.find_element(select_locator)
        options = select.find_elements(*PageElement.by_css_selector("option"))
        for option in options:
            if value in option.text:
                option.click()
                break
