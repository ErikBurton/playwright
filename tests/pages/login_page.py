from playwright.sync_api import expect
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.submit = page.locator("button[type='submit']")
        self.flash_message = page.locator("#flash")

    def navigate(self):
        self.page.goto("https://the-internet.herokuapp.com/login")

    def login(self, user, password):
        self.username.fill(user)
        self.password.fill(password)
        self.submit.click()

    def expect_flash_contains(self, text):
        expect(self.flash_message).to_contain_text(text)

