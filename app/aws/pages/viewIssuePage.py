from .loggedInPage import LoggedInPage
from .pageElements import PageElement, PageFieldElement


class ViewIssuePage(LoggedInPage):

    __RESOLVE_BUTTON = PageElement.by_link_text("Resolved")
    __IN_PROGRESS_BUTTON = PageElement.by_link_text("In Progress")
    __ISSUE_KEY = PageElement.by_css_selector("a#key-val")
    __PROJECT_FILTER = PageElement.by_css_selector('.criteria-list [data-id="project"]')
    __PROJECT_FILTER_FIELD = PageElement.by_css_selector("form.project-criteria input")
    __FILTERED_PROJECTS = PageElement.by_css_selector("form.project-criteria label")

    __project_filter_field = PageFieldElement(__PROJECT_FILTER_FIELD)

    @property
    def issue_key(self):
        return self.find_element(self.__ISSUE_KEY).text

    def resolve(self):
        self.click(self.__RESOLVE_BUTTON)

    def in_progress(self):
        self.click(self.__IN_PROGRESS_BUTTON)

    def filter_project(self, project_key: str) -> None:
        self.click(self.__PROJECT_FILTER)
        self.__project_filter_field = project_key
        filtered_projects = self.find_elements(self.__FILTERED_PROJECTS)
        for project in filtered_projects:
            if f"({project_key})" in project.text:
                project.click()
                break
        self.click(self.__PROJECT_FILTER)

    def filter_type(self, issue_type: str) -> None:
        # TODO
        pass

    def filter_status(self, status: str) -> None:
        # TODO
        pass
