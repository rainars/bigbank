from behave import given, when, then
from config import Config
from pages.loan_calculator_page import LoanCalculatorPage


@given("the loan calculator page is opened")
def open_loan_calculator_page(context):
    context.page = context.browser.new_page()
    context.loan_calculator = LoanCalculatorPage(context.page)
    context.loan_calculator.open(Config.LOAN_CALCULATOR_URL)

@when('I set the loan amount to "{amount}"')
def set_loan_amount(context, amount):
    scenario_name = context.scenario.name  # Capture scenario name
    context.loan_calculator.set_loan_amount(amount, scenario_name)

@when('I set the loan period to "{period}"')
def set_loan_period(context, period):
    scenario_name = context.scenario.name  # Correct variable name
    context.loan_calculator.set_loan_period(period, scenario_name)

@when("I close the loan calculator without saving")
def close_modal_without_saving(context):
    context.loan_calculator.close_modal_without_saving()

@when("I reopen the loan calculator")
def reopen_loan_calculator(context):
    context.loan_calculator.click_edit_amount_button()
    print("✅ Clicked Edit Button to reopen calculator")
    context.page.wait_for_selector("input[name='header-calculator-amount']", state="visible")
    print("✅ Loan calculator modal reopened successfully")

@then("the loan amount should be the default value")
def verify_default_loan_amount(context):
    loan_amount = context.loan_calculator.get_loan_amount()
    assert loan_amount == "5,000", f"❌ Expected default loan amount '5000', but got '{loan_amount}'"


@then("the loan period should be the default value")
def verify_default_loan_period(context):
    loan_period = context.loan_calculator.get_loan_period()
    assert loan_period == "60", f"❌ Expected default loan period '60', but got '{loan_period}'"


@when("I click the save button")
def click_save_button(context):
    context.loan_calculator.click_save_button()
    context.page.wait_for_timeout(1000)  # Allow data to save before validation
    print("✅ Saved loan data by clicking the save button.")


@then("the loan amount should be \"{expected_amount}\"")
def verify_saved_loan_amount(context, expected_amount):
    loan_amount = context.loan_calculator.get_loan_amount()
    assert loan_amount == expected_amount, f"❌ Expected loan amount '{expected_amount}', but got '{loan_amount}'"


@then('the monthly payment should not be invalid')
def verify_monthly_payment(context):
    """Validates the monthly payment is a valid positive number (not zero, negative, empty, or non-numeric)."""

    # Get the displayed monthly payment value
    monthly_payment_raw = context.loan_calculator.get_monthly_payment()
    print(f"🔍 Displayed Monthly Payment: {monthly_payment_raw}")

    # Remove currency symbols (€ or $) and commas (for thousands formatting)
    monthly_payment_cleaned = monthly_payment_raw.replace("€", "").replace(",", "").strip()

    try:
        # Convert cleaned value to float
        monthly_payment = float(monthly_payment_cleaned)

        # Perform assertions
        assert monthly_payment > 0, f"❌ Monthly payment must be greater than zero, but got {monthly_payment}"
        assert isinstance(monthly_payment,
                          (int, float)), f"❌ Monthly payment must be a number, but got {type(monthly_payment).__name__}"

    except ValueError:
        raise AssertionError(f"❌ Monthly payment is NOT a valid number: {monthly_payment_raw}")

    print(f"✅ Valid Monthly Payment: {monthly_payment}")


@then('the loan amount "{value}" should persist after saving')
def verify_loan_amount_persistence(context, value):
    """Verifies that the loan amount persists after saving and reopening, handling formatting issues."""

    # Fetch the saved loan amount after reopening
    saved_amount = context.loan_calculator.get_loan_amount()

    # Remove thousand separators (commas) from both saved and expected values
    saved_amount_clean = saved_amount.replace(",", "")
    expected_amount_clean = value.replace(",", "")

    assert saved_amount_clean == expected_amount_clean, (
        f"❌ Expected loan amount '{expected_amount_clean}', but got '{saved_amount_clean}'"
    )
    print(f"✅ Loan amount persisted correctly: {saved_amount_clean}")


@then("the calculated monthly payment should match the API result")
def verify_payment_matches_api(context):
    # Extract displayed UI monthly payment
    displayed_payment = context.loan_calculator.get_monthly_payment().replace("€", "").strip()
    displayed_payment = round(float(displayed_payment), 2)

    print(f"Displayed Payment: {displayed_payment}, API Payment: {context.api_monthly_payment}")

    # Ensure API step ran before this step
    assert hasattr(context,
                   "api_monthly_payment"), "API response data is missing. Ensure API step runs before this step."

    # Assert API and UI monthly payments match
    assert displayed_payment == round(float(context.api_monthly_payment), 2), (
        f"Displayed payment ({displayed_payment}) does not match API payment ({context.api_monthly_payment})"
    )
