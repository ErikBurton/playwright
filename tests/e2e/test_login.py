from pages.login_page import LoginPage
from playwright.sync_api import expect


def test_user_can_login(page):
    login = LoginPage(page)
    login.navigate()
    login.login("tomsmith", "SuperSecretPassword!")

    login.expect_flash_contains("You logged into a secure area!")
