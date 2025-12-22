import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = Path("screenshots")
VIDEOS_DIR = Path("videos")


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture
def context(browser):
    VIDEOS_DIR.mkdir(exist_ok=True)

    context = browser.new_context(
        record_video_dir=VIDEOS_DIR,
        record_video_size={"width": 1280, "height": 720},
    )

    yield context
    context.close()


@pytest.fixture
def page(context, request):
    page = context.new_page()
    yield page

    rep = getattr(request.node, "rep_call", None)
    failed = rep.failed if rep else False

    if page.video:
        video_path = page.video.path()

        if not failed:
            Path(video_path).unlink(missing_ok=True)


@pytest.fixture(scope="session")
def api_context(playwright):
    request_context = playwright.request.new_context(
        base_url="https://the-internet.herokuapp.com"
    )
    yield request_context
    request_context.dispose()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            SCREENSHOTS_DIR.mkdir(exist_ok=True)
            page.screenshot(path=SCREENSHOTS_DIR / f"{item.name}.png")
