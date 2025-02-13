from playwright.sync_api import sync_playwright


def before_all(context):
    # Start Playwright and open the browser
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=True, slow_mo=500)  # Set headless=True if needed


def after_all(context):
    # Close the browser and stop Playwright
    context.browser.close()
    context.playwright.stop()
