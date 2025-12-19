import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path

SCREENSHOTS_DIR = Path("screenshots")


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            SCREENSHOTS_DIR.mkdir(exist_ok=True)
            screenshot_path = SCREENSHOTS_DIR / f"{item.name}.png"
            page.screenshot(path=screenshot_path)
