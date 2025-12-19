from pages.login_page import LoginPage
from playwright.sync_api import expect


def test_user_cannot_login_with_valid_credentials(page):
    login = LoginPage(page)
    login.navigate()
    login.login("invalid_user", "wrong_password")

    login.expect_flash_contains("Your username is invalid!")
