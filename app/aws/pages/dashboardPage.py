from .loggedInPage import LoggedInPage


class DashboardPage(LoggedInPage):

    def is_title_matches(self):
        return "<h1>System Dashboard</h1>" in self.page_source
