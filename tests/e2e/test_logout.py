from pages.login_page import LoginPage
from pages.secure_page import SecurePage


def test_user_can_logout(page):
    login = LoginPage(page)
    secure = SecurePage(page)

    login.navigate()
    login.login("tomsmith", "SuperSecretPassword!")

    secure.expect_on_secure_page()
    secure.logout()
    secure.expect_logged_out_message()
