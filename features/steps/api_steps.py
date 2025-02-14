import requests
from behave import when, then
from features.config import Config  # Import Config class

API_URL = Config.LOAN_CALCULATOR_API  # Use the URL from config
#API_URL = "https://taotlus.bigbank.ee/api/v1/loan/calculate"
@when('I send a loan calculation request with amount "{amount}" and period "{period}"')
def send_loan_calculation_request(context, amount, period):
    try:
        payload = {
            "currency": "EUR",
            "productType": "SMALL_LOAN_EE01",
            "maturity": int(period) if period.isdigit() else period,
            "administrationFee": 3.99,
            "conclusionFee": 100,
            "amount": int(amount) if amount.isdigit() else amount,
            "monthlyPaymentDay": 15,
            "interestRate": 15.1
        }

        response = requests.post(API_URL, json=payload)
        context.api_status_code = response.status_code
        context.api_response = response.json()  # Only call once

        print(f"API Response: {context.api_response}")

        # If API response is a list, extract the first element
        if isinstance(context.api_response, list):
            if context.api_response:  # Check if the list is not empty
                context.api_response_data = context.api_response[0]  # Take the first dictionary
            else:
                raise AssertionError("API response is an empty list")
        else:
            context.api_response_data = context.api_response

        # Store values for later validation
        context.api_monthly_payment = context.api_response_data.get("monthlyPayment")
        context.api_apr = context.api_response_data.get("apr")

    except Exception as e:
        context.api_response = None
        print(f"Error in API call: {e}")


@then("the API should return a valid monthly payment and APRC")
def validate_api_response(context):
    """Validates the API response contains a total repayable amount, monthly payment, and APRC."""
    assert context.api_response is not None, "❌ No response received from API"

    # Ensure required fields exist in response
    assert "monthlyPayment" in context.api_response, "❌ API response missing 'monthlyPayment' key"
    assert "apr" in context.api_response, "❌ API response missing 'apr' key"
    assert "totalRepayableAmount" in context.api_response, "❌ API response missing 'totalRepayableAmount' key"

    # Extract values
    context.api_monthly_payment = round(float(context.api_response.get("monthlyPayment", 0)), 2)
    context.api_apr = round(float(context.api_response.get("apr", 0)), 2)
    context.api_total_repayable = round(float(context.api_response.get("totalRepayableAmount", 0)), 2)

    # Print API response values
    print(f"✅ API Monthly Payment: {context.api_monthly_payment}, API APRC: {context.api_apr}, API Total Repayable Amount: {context.api_total_repayable}")

    # Ensure values are valid (non-zero and not empty)
    assert context.api_monthly_payment > 0, f"❌ Invalid API Monthly Payment: {context.api_monthly_payment}"
    assert context.api_apr > 0, f"❌ Invalid API APRC: {context.api_apr}"
    assert context.api_total_repayable > 0, f"❌ Invalid API Total Repayable Amount: {context.api_total_repayable}"



@then("the API should return an error response")
def validate_error_response(context):
    assert context.api_status_code == 500, f"Expected status 500, but got {context.api_status_code}"
    assert "error" in context.api_response or "message" in context.api_response, "No error message received"
    print(f"API Error Response: {context.api_response}")


@then("the API should return an error for non-numeric amount")
def step_verify_amount_error(context):
    assert isinstance(context.api_response, list), f"Expected a list but got {type(context.api_response)}"

    error = context.api_response_data  # Now we use this safely

    #assert error["dataPath"] == ".amount", f"Unexpected data path: {error['dataPath']}"
    #assert error["params"]["type"] == "number", f"Expected 'number', got {error['params']['type']}"
    assert "should be number" in error["message"], f"Unexpected message: {error['message']}"




