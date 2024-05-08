from .loggedInPage import LoggedInPage
from .pageElements import PageElement, PageFieldElement


class CreateIssueFirstPage(LoggedInPage):

    __PROJECT_FIELD = PageElement.by_css_selector('#project-single-select input')
    __ISSUE_TYPE_FIELD = PageElement.by_css_selector('#issuetype-single-select input')

    __project = PageFieldElement(__PROJECT_FIELD)
    __issue_type = PageFieldElement(__ISSUE_TYPE_FIELD)

    def next(self) -> None:
        self.submit(PageElement.by_css_selector("form#issue-create"))

    def set_project(self, project_key: str):
        print("FOO")
        project_list = self.find_element(PageElement.by_css_selector("#project-single-select > span"))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", project_list)
        self.click(project_list)
        if f"({project_key})" not in self.__project:
            aws_project = self.find_element(PageElement.by_partial_link_text(f"({project_key})"))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", project_list)
            self.click(aws_project)
            #self.click(PageElement.by_partial_link_text(project_key))
        else:
            self.click(project_list)
        
    def set_issue_type(self, issue_type: str):
        self.click(PageElement.by_css_selector("#issuetype-single-select > span"))
        if issue_type not in self.__issue_type:
            self.click(PageElement.by_link_text(issue_type))
        else:
            self.click(PageElement.by_css_selector("#issuetype-single-select > span"))
