import pytest
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", default=False)
    parser.addoption("--slowmo", action="store", default=0, type=int)
    parser.addoption("--screenshot", action="store", default="off")
    parser.addoption("--video", action="store_true", default=False)


@pytest.fixture
def page(request):
    headed = request.config.getoption("--headed")
    slowmo = request.config.getoption("--slowmo")
    screenshot = request.config.getoption("--screenshot")
    video = request.config.getoption("--video")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=not headed,
            slow_mo=slowmo
        )

        context_args = {}

        if video:
            context_args["record_video_dir"] = "playwright/videos"

        context = browser.new_context(**context_args)
        page = context.new_page()

        yield page

        if screenshot == "on":
            page.screenshot(path="playwright/screenshots/final.png")

        context.close()
        browser.close()
