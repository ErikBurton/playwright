from playwright.sync_api import expect
import re


class SecurePage:
    def __init__(self, page):
        self.page = page

        # Locators
        self.logout_button = page.locator("a[href='/logout']")
        self.flash_message = page.locator("#flash")

    def expect_on_secure_page(self):
        expect(self.page).to_have_url(re.compile(".*/secure$"))

    def logout(self):
        self.logout_button.click()

    def expect_logged_out_message(self):
        expect(self.flash_message).to_contain_text(
            "You logged out of the secure area!"
        )
