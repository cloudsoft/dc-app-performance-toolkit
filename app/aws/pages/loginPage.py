from .basePage import BasePage
from .pageElements import PageFieldElement, PageElement


class LoginPage(BasePage):
    USERNAME_FIELD = PageElement.by_css_selector("#login-form-username")
    PASSWORD_FIELD = PageElement.by_css_selector("#login-form-password")
    LOGIN_BUTTON = PageElement.by_css_selector("#login")

    username = PageFieldElement(USERNAME_FIELD)
    password = PageFieldElement(PASSWORD_FIELD)

    def click_login_button(self) -> None:
        self.click(self.LOGIN_BUTTON)

    def login_as(self, username: str, password: str):
        self.username = username
        self.password = password
        self.click_login_button()
