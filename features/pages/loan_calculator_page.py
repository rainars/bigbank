from locators import LoanCalculatorLocators


class LoanCalculatorPage:
    def __init__(self, page):
        self.page = page
        self.loan_amount_input = self.page.locator(LoanCalculatorLocators.LOAN_AMOUNT_INPUT)
        self.loan_period_input = self.page.locator(LoanCalculatorLocators.LOAN_PERIOD_INPUT)
        self.monthly_payment_locator = self.page.locator(LoanCalculatorLocators.MONTHLY_PAYMENT)
        self.save_button = self.page.locator(LoanCalculatorLocators.SAVE_BUTTON)
        # self.page.locator("//span[text()='JÄTKA']/ancestor::button").click()
        self.close_button =  self.page.locator(LoanCalculatorLocators.CLOSE_BUTTON)

    def open(self, url):
        self.page.goto(url)

    def set_loan_amount(self, amount):
        self.loan_amount_input.fill(str(amount))
        self.page.wait_for_selector(LoanCalculatorLocators.WAIT_FOR_MONTHLY_PAYMENT)
        self.page.click(LoanCalculatorLocators.BODY)

    def set_loan_period(self, period):
        self.loan_period_input.fill(str(period))
        self.page.wait_for_selector(LoanCalculatorLocators.WAIT_FOR_MONTHLY_PAYMENT)
        self.page.click(LoanCalculatorLocators.BODY)

    def get_monthly_payment(self):
        self.monthly_payment_locator.wait_for(state="visible", timeout=5000)
        return self.monthly_payment_locator.text_content().strip()

    def close_modal_without_saving(self):
        """ Closes the modal without clicking Save """
        self.close_button.click()
        self.page.wait_for_timeout(500)  # Ensure modal is fully closed

    def reopen(self):
        """ Opens the loan calculator modal """
        self.page.goto(
            "https://taotlus.bigbank.ee/?amount=5000&period=60&productName=SMALL_LOAN&loanPurpose=DAILY_SETTLEMENTS")
        self.page.wait_for_selector("text=Vali sobiv summa ja periood")

    def get_loan_amount(self):
        """ Retrieves the current value of the loan amount field """
        return self.loan_amount_input.input_value().strip()

    def get_loan_period(self):
        """ Retrieves the current value of the loan period field """
        return self.loan_period_input.input_value().strip()

    def click_save_button(self):
        """Clicks the enabled save button in the modal."""

        # Wait for the modal to be visible
        self.page.wait_for_selector("button.bb-calculator-modal__submit-button", state="visible")

        # Locate the enabled save button (JÄTKA)
        save_button = self.page.locator("button.bb-calculator-modal__submit-button:not([disabled])")

        # Backup locator for JÄTKA button (if different structure)
        self.save_button = self.page.locator("button:has-text('JÄTKA')")

        # Ensure the button exists and is clickable
        if save_button.count() > 0 and save_button.is_visible():
            save_button.click()
            print("✅ Clicked on Save Button (JÄTKA)")
        else:
            raise Exception("❌ Save button is either missing or still disabled.")

    def save_loan_settings(self):
        self.page.click("button:has(span.bb-button__label:text('JÄTKA'))")

    def click_edit_amount_button(self):
        """Waits for and clicks the 'Edit Amount' button in the navbar."""
        edit_button = self.page.locator("button.bb-edit-amount")  # Correct class name

        # Debugging: Check if the button exists
        if edit_button.count() == 0:
            raise Exception("❌ Edit Amount button not found!")

        edit_button.wait_for(state="visible", timeout=5000)  # Ensure it's visible
        edit_button.click()
        print("✅ Clicked on Edit Amount Button")
