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
    """Validates the API response contains correct loan calculation values and ensures numeric types."""

    # Ensure API response exists
    assert context.api_response is not None, "❌ API response is missing!"

    # Define expected keys and their types
    expected_keys = {
        "monthlyPayment": float,
        "apr": float,
        "totalRepayableAmount": float
    }

    # Validate presence of required keys
    missing_keys = [key for key in expected_keys if key not in context.api_response]
    assert not missing_keys, f"❌ API response is missing keys: {missing_keys}"

    try:
        # Extract values and enforce correct data types
        for key, expected_type in expected_keys.items():
            value = context.api_response[key]

            # Ensure the value is numeric and not a string
            if isinstance(value, str) or not isinstance(value, (int, float)):
                raise TypeError(f"❌ Expected numeric type for '{key}', but got {type(value).__name__} with value: {value}")

            # Store values in context with correct naming
            setattr(context, f"api_{key}", round(expected_type(value), 2))

        # Debugging output
        print(f"✅ API Response Received:")
        print(f"   - Monthly Payment: {context.api_monthlyPayment}")
        print(f"   - APRC: {context.api_apr}")
        print(f"   - Total Repayable Amount: {context.api_totalRepayableAmount}")

        # Ensure values are positive and non-zero
        assert context.api_monthlyPayment > 0, f"❌ Monthly Payment must be greater than 0, got {context.api_monthlyPayment}"
        assert context.api_apr > 0, f"❌ APRC must be greater than 0, got {context.api_apr}"
        assert context.api_totalRepayableAmount > 0, f"❌ Total Repayable Amount must be greater than 0, got {context.api_totalRepayableAmount}"

    except TypeError as e:
        if not hasattr(context, "failed"):
            context.failed = False  # Initialize `context.failed` if missing
        context.failed = True
        raise AssertionError(f"❌ Data Type Error: {e}")

    except KeyError as e:
        if not hasattr(context, "failed"):
            context.failed = False  # Initialize `context.failed` if missing
        context.failed = True
        raise AssertionError(f"❌ Missing expected key in API response: {e}")

    except ValueError as e:
        if not hasattr(context, "failed"):
            context.failed = False
        context.failed = True
        raise AssertionError(f"❌ API returned invalid numerical values: {e}")

    except Exception as e:
        if not hasattr(context, "failed"):
            context.failed = False
        context.failed = True
        raise AssertionError(f"❌ Unexpected error while processing API response: {e}")




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




