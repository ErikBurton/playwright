import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = Path("screenshots")
VIDEOS_DIR = Path("videos")


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
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

    # IMPORTANT: context must close to finalize video
    context.close()


@pytest.fixture
def page(context, request):
    page = context.new_page()
    yield page

    # Only after test execution
    rep = getattr(request.node, "rep_call", None)
    failed = rep.failed if rep else False

    if page.video:
        video_path = page.video.path()

        if failed:
            # keep video
            print(f"🎥 Saved video: {video_path}")
        else:
            # delete video if test passed
            Path(video_path).unlink(missing_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            SCREENSHOTS_DIR.mkdir(exist_ok=True)
            screenshot_path = SCREENSHOTS_DIR / f"{item.name}.png"
            page.screenshot(path=screenshot_path)
