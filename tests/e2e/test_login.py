from pages.login_page import LoginPage


def test_user_can_login(page):
    login = LoginPage(page)
    login.navigate()
    login.login("tomsmith", "SuperSecretPassword!")

    assert "secure" in page.url
