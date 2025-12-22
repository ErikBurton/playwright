from playwright.sync_api import expect

def test_login_via_api_then_open_secure_page(context, page):
    context.request.post(
        "https://the-internet.herokuapp.com/authenticate",
        form={
            "username": "tomsmith",
            "password": "SuperSecretPassword!"
        }
    )

    page.goto("https://the-internet.herokuapp.com/secure")

    expect(page.locator("h2")).to_have_text("Secure Area")
