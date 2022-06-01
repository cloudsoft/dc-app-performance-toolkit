from .loggedInPage import LoggedInPage
from .pageElements import PageElement, PageFieldElement


class CreateIssueFirstPage(LoggedInPage):

    __PROJECT_FIELD = PageElement.by_css_selector('#project-single-select input')
    __ISSUE_TYPE_FIELD = PageElement.by_css_selector('#issuetype-single-select input')

    __project = PageFieldElement(__PROJECT_FIELD)
    __issue_type = PageFieldElement(__ISSUE_TYPE_FIELD)

    def next(self) -> None:
        self.submit(PageElement.by_css_selector("form#issue-create"))