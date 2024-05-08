from .loggedInPage import LoggedInPage
from .pageElements import PageElement, PageFieldElement


class CreateIssueSecondPage(LoggedInPage):

    __SUMMARY_FIELD = PageElement.by_css_selector("#summary")
    __DESCRIPTION_VISUAL_TAB =\
        PageElement.by_css_selector('#description-wiki-edit > nav > div > div > ul > li:nth-child(1) > button')
    __DESCRIPTION_TEXT_TAB =\
        PageElement.by_css_selector('#description-wiki-edit > nav > div > div > ul > li:nth-child(2) > button')
    __DESCRIPTION_FIELD = PageElement.by_css_selector("#description")

    __summary = PageFieldElement(__SUMMARY_FIELD)
    __description = PageFieldElement(__DESCRIPTION_FIELD)

    def set_summary(self, text: str) -> None:
        self.__summary = text

    def set_description(self, text: str) -> None:
        self.click(self.__DESCRIPTION_TEXT_TAB)
        self.__description = text
        self.click(self.__DESCRIPTION_VISUAL_TAB)

    def create(self) -> None:
        self.submit(PageElement.by_css_selector("form#issue-create"))

