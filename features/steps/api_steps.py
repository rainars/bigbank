import json
import requests
from behave import when, then
from features.config import Config  # Import Config class

API_URL = Config.LOAN_CALCULATOR_API  # Use the URL from config


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


@when('I send a loan calculation request with')
def send_loan_calculation_request_docString(context):
    """Handles API requests using JSON from DocString."""
    try:
        # Debugging: Print raw input to check formatting issues
        # print(f"📜 Raw JSON Input: {context.text}")

        # Parse JSON from DocString
        payload = json.loads(context.text)

        # Send API Request
        response = requests.post(API_URL, json=payload)
        context.api_status_code = response.status_code
        context.api_response = response.json()


    except json.JSONDecodeError as e:
        # print(f"❌ JSON Parsing Error: {e}")
        context.api_response = None


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
                raise TypeError(
                    f"❌ Expected numeric type for '{key}', but got {type(value).__name__} with value: {value}")

            # Store values in context with correct naming
            setattr(context, f"api_{key}", round(expected_type(value), 2))

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


@then("the API should return an error for non-numeric amount")
def step_verify_amount_error(context):
    """Validates API error response for non-numeric amounts."""

    # Ensure API response exists
    assert context.api_response is not None, "❌ API response is None. Possible API failure."

    # Check if API response is a list or dict
    if isinstance(context.api_response, list):
        error = context.api_response[0] if context.api_response else None
    else:
        error = context.api_response  # If it's not a list, assume it's a dict

    # Ensure the response contains an error message
    assert error is not None, "❌ API did not return a valid error message."
    assert "message" in error, f"❌ Missing 'message' in API response: {error}"

    # Validate error message
    expected_message = "should be number"
    assert expected_message in error["message"], f"❌ Unexpected error message: {error['message']}"


@then('the API should return status code {expected_status:d}')
def verify_api_status_code(context, expected_status):
    """Ensures the API returns the expected HTTP status code."""

    # Ensure the API response exists
    assert hasattr(context, "api_status_code"), "❌ API status code is missing in context. Ensure API step runs first."

    # Convert expected_status to integer (Behave passes it as a string)
    expected_status = int(expected_status)

    # Validate the actual status code against the expected one
    assert context.api_status_code == expected_status, (
        f"❌ Expected status code {expected_status}, but got {context.api_status_code}"
    )


@then("the API response should contain")
def verify_api_response_structure(context):
    """
    Ensures that the API response contains the expected keys and correct data types.
    """
    # Ensure API response exists
    assert hasattr(context, "api_response"), "❌ API response is missing! Ensure API request was made first."

    # Convert table into expected key-type mapping
    expected_structure = {}
    for row in context.table:
        expected_structure[row["key"]] = row["type"]

    # Validate each expected key exists and matches the expected type
    for key, expected_type in expected_structure.items():
        assert key in context.api_response, f"❌ Missing expected key: '{key}' in API response."

        actual_value = context.api_response[key]
        expected_python_type = {"int": int, "float": float, "string": str, "bool": bool}[expected_type]

        # Type validation
        assert isinstance(actual_value, expected_python_type), (
            f"❌ Expected '{key}' to be {expected_type}, but got {type(actual_value).__name__}"
        )
