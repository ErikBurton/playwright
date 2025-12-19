from pages.login_page import LoginPage


def test_user_can_login(page):
    login = LoginPage(page)
    login.navigate()
    login.login("tomsmith", "SuperSecretPassword!")

    # login.expect_flash_contains("You logged into a secure area!")
    login.expect_flash_contains("THIS WILL FAIL!")
