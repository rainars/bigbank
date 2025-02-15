class LoanCalculatorLocators:
    LOAN_AMOUNT_INPUT = 'input[name="header-calculator-amount"]'
    LOAN_PERIOD_INPUT = 'input[name="header-calculator-period"]'
    MONTHLY_PAYMENT = "p.bb-labeled-value__value"
    # Buttons
    SAVE_BUTTON = "button:has-text('JÄTKA')"  # Save button
    CLOSE_BUTTON = "button.bb-modal__close"  # Modal close button
    EDIT_AMOUNT_BUTTON = "button.bb-edit-amount"  # Edit amount button
    # General actions
    WAIT_FOR_MONTHLY_PAYMENT = "p.bb-labeled-value__value:visible"
    BODY = "body"
    # Submit button inside the modal (JÄTKA button)
    MODAL_SUBMIT_BUTTON = "button.bb-calculator-modal__submit-button"
    # Enabled Save button (JÄTKA button that is not disabled)
    ENABLED_SAVE_BUTTON = "button.bb-calculator-modal__submit-button:not([disabled])"