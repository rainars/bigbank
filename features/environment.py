from playwright.sync_api import sync_playwright
import os
import allure


def before_all(context):
    # Start Playwright and open the browser
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=True, slow_mo=500)  # Set headless=True if needed

def after_step(context, step):
    """Attach failure details (screenshots & logs) to Allure on step failure."""
    if step.status == "failed":
        # Save failure log
        log_message = f"Step failed: {step.name}\nException: {step.exception}"
        log_path = f"test-reports/allure-results/failure_logs/{context.scenario.name}.txt"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        with open(log_path, "w", encoding="utf-8") as log_file:
            log_file.write(log_message)

        # Attach log file to Allure
        allure.attach.file(log_path, name="Failure Log", attachment_type=allure.attachment_type.TEXT)

        # Capture screenshot if browser is available
        if hasattr(context, "page") and context.page:
            screenshot_path = f"test-reports/allure-results/failure_screenshots/{context.scenario.name}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

            context.page.screenshot(path=screenshot_path)

            # Attach screenshot to Allure
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)

            print(f"📸 Screenshot saved at: {screenshot_path}")
        else:
            print("⚠️ No page instance found. Cannot take a screenshot.")


def after_all(context):
    # Close the browser and stop Playwright
    context.browser.close()
    context.playwright.stop()
