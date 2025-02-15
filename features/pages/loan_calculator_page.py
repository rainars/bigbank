import re
from locators import LoanCalculatorLocators


class LoanCalculatorPage:
    def __init__(self, page):
        self.page = page
        self.loan_amount_input = self.page.locator(LoanCalculatorLocators.LOAN_AMOUNT_INPUT)
        self.loan_period_input = self.page.locator(LoanCalculatorLocators.LOAN_PERIOD_INPUT)
        self.monthly_payment_locator = self.page.locator(LoanCalculatorLocators.MONTHLY_PAYMENT)
        self.save_button = self.page.locator(LoanCalculatorLocators.SAVE_BUTTON)
        self.close_button = self.page.locator(LoanCalculatorLocators.CLOSE_BUTTON)

    def open(self, url):
        self.page.goto(url)

    def set_loan_amount(self, amount, scenario_name):
        """Sets the loan amount and verifies it unless it's an edge case scenario."""
        self.loan_amount_input.fill(str(amount))
        self.page.wait_for_selector(LoanCalculatorLocators.WAIT_FOR_MONTHLY_PAYMENT)
        self.page.click(LoanCalculatorLocators.BODY)

        # Get actual value from input field
        actual_amount = self.loan_amount_input.input_value()

        # Normalize values (remove thousands separators)
        normalized_actual = re.sub(r"[,.]", "", actual_amount)
        normalized_expected = str(amount)

        # Skip assertion if it's the "Edge cases" scenario
        if "Edge cases" not in scenario_name:
            assert normalized_actual == normalized_expected, f"Expected loan amount {normalized_expected}, but got {normalized_actual}"

    def set_loan_period(self, period, scenario_name):
        self.loan_period_input.fill(str(period))
        self.page.wait_for_selector(LoanCalculatorLocators.WAIT_FOR_MONTHLY_PAYMENT)
        self.page.click(LoanCalculatorLocators.BODY)
        # Verify that the input field contains the correct period
        actual_period = self.loan_period_input.input_value()
        # Skip assertion if it's the "Edge cases" scenario
        if "Edge cases" not in scenario_name:
            assert actual_period == str(period), f"Expected loan period {period}, but got {actual_period}"

    def get_monthly_payment(self):
        self.monthly_payment_locator.wait_for(state="visible", timeout=5000)
        return self.monthly_payment_locator.text_content().strip()

    def close_modal_without_saving(self):
        """ Closes the modal without clicking Save """
        self.close_button.click()
        self.page.wait_for_timeout(500)  # Ensure modal is fully closed

    def get_loan_amount(self):
        """ Retrieves the current value of the loan amount field """
        return self.loan_amount_input.input_value().strip()

    def get_loan_period(self):
        """ Retrieves the current value of the loan period field """
        return self.loan_period_input.input_value().strip()

    def click_save_button(self):
        """Clicks the enabled save button in the modal."""

        # Wait for the modal to be visible
        self.page.wait_for_selector(LoanCalculatorLocators.MODAL_SUBMIT_BUTTON, state="visible")

        # Locate the enabled save button (JÄTKA)
        save_button = self.page.locator(LoanCalculatorLocators.ENABLED_SAVE_BUTTON)

        # Backup locator for JÄTKA button (if different structure)
        self.save_button = self.page.locator(LoanCalculatorLocators.SAVE_BUTTON)

        # Ensure the button exists and is clickable
        if save_button.count() > 0 and save_button.is_visible():
            save_button.click()

        else:
            raise Exception("❌ Save button is either missing or still disabled.")

    def click_edit_amount_button(self):
        """Waits for and clicks the 'Edit Amount' button in the navbar."""
        edit_button = self.page.locator(LoanCalculatorLocators.EDIT_AMOUNT_BUTTON)  # Correct class name

        # Debugging: Check if the button exists
        if edit_button.count() == 0:
            raise Exception("❌ Edit Amount button not found!")

        edit_button.wait_for(state="visible", timeout=5000)  # Ensure it's visible
        edit_button.click()
