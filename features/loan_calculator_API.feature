Feature: Loan Calculator Monthly Payment API

  Scenario Outline: Validate extreme values for loan calculation
    When I send a loan calculation request with
  """
  {
    "currency": "EUR",
    "productType": "SMALL_LOAN_EE01",
    "maturity": <period>,
    "administrationFee": 3.99,
    "conclusionFee": 100,
    "amount": <amount>,
    "monthlyPaymentDay": 15,
    "interestRate": 15.1
  }
  """
    Then the API should return a valid monthly payment and APRC

    Examples:
      | amount | period |
      | 1      | 12     |
      | 999999 | 120    |
      | 5000   | 1      |
      | 5000   | 360    |
      | 5000   | 60     |


  Scenario Outline: Validate loan calculations for different values
       When I send a loan calculation request with
  """
  {
    "currency": "EUR",
    "productType": "SMALL_LOAN_EE01",
    "maturity": <period>,
    "administrationFee": 3.99,
    "conclusionFee": 100,
    "amount": <amount>,
    "monthlyPaymentDay": 15,
    "interestRate": 15.1
  }
  """
    Then the API should return a valid monthly payment and APRC

    Examples:
      | amount | period |
      | 1000   | 12     |
      | 2000   | 24     |
      | 5000   | 36     |
      | 10000  | 48     |
      | 20000  | 60     |


  Scenario Outline: Validate API rejects non-numeric values
       When I send a loan calculation request with
  """
  {
    "currency": "EUR",
    "productType": "SMALL_LOAN_EE01",
    "maturity": <period>,
    "administrationFee": 3.99,
    "conclusionFee": 100,
    "amount": <amount>,
    "monthlyPaymentDay": 15,
    "interestRate": 15.1
  }
  """
    Then the API should return an error for non-numeric amount
#
    Examples:
      | amount | period |
      | "abc"  | 60     |
      | 5000   | "abc"  |
      | "abc"  | "abc"  |
      | ""     | 60     |
      | 5000   | ""     |
      | ""     | ""     |


  Scenario Outline: Validate API rejects negative and zero values
        When I send a loan calculation request with
  """
  {
    "currency": "EUR",
    "productType": "SMALL_LOAN_EE01",
    "maturity": <period>,
    "administrationFee": 3.99,
    "conclusionFee": 100,
    "amount": <amount>,
    "monthlyPaymentDay": 15,
    "interestRate": 15.1
  }
  """
   # Then the API should return an error for invalid loan parameters

    Examples:
      | amount | period |
      | -5000  | 12     |
      | 5000   | -12    |
      | -5000  | -12    |
      | 0      | 12     |
      | 5000   | 0      |
      | 0      | 0      |

  Scenario Outline: Validate API handles maximum and minimum limits
        When I send a loan calculation request with
  """
  {
    "currency": "EUR",
    "productType": "SMALL_LOAN_EE01",
    "maturity": <period>,
    "administrationFee": 3.99,
    "conclusionFee": 100,
    "amount": <amount>,
    "monthlyPaymentDay": 15,
    "interestRate": 15.1
  }
  """
    Then the API should return a valid monthly payment and APRC

    Examples:
      | amount  | period | description      |
      | 100     | 1      |                  |
      | 1000000 | 240    |                  |
      | 5000    | 180    | Mid-range period |


  Scenario Outline: Validate API handles decimal values
        When I send a loan calculation request with
  """
  {
    "currency": "EUR",
    "productType": "SMALL_LOAN_EE01",
    "maturity": <period>,
    "administrationFee": 3.99,
    "conclusionFee": 100,
    "amount": <amount>,
    "monthlyPaymentDay": 15,
    "interestRate": 15.1
  }
  """
    #Then the API should return an error or round appropriately

    Examples:
      | amount   | period |
      | 1000.50  | 12     |
      | 5000.75  | 24     |
      | 99999.99 | 60     |
      | 10000    | 12.5   |
      | 20000.99 | 36     |

  Scenario Outline: Validate API rejects special characters
        When I send a loan calculation request with
  """
  {
    "currency": "EUR",
    "productType": "SMALL_LOAN_EE01",
    "maturity": <period>,
    "administrationFee": 3.99,
    "conclusionFee": 100,
    "amount": <amount>,
    "monthlyPaymentDay": 15,
    "interestRate": 15.1
  }
  """
    Then the API should return an error for non-numeric amount

    Examples:
      | amount | period |
      | "!!!"  | 12     |
      | 5000   | "@@"   |
      | "###"  | "!!"   |
      | null   | 12     |
      | 5000   | null   |

  Scenario Outline: Validate API handles valid interest rates correctly
    When I send a loan calculation request with
  """
  {
    "currency": "EUR",
    "productType": "SMALL_LOAN_EE01",
    "maturity": 12,
    "administrationFee": 3.99,
    "conclusionFee": 100,
    "amount": 5000,
    "monthlyPaymentDay": 15,
    "interestRate": <interestRate>
  }
  """
    Then the API should return a valid monthly payment and APRC

    Examples:
      | interestRate | description                                  |
      | 0.1          | # Minimal positive interest rate             |
      | 5.5          | # Standard interest rate                     |
      | 15.1         | # Given valid interest rate from API request |
      | 25.0         | # High valid interest rate                   |
      | 50.0         | # Edge case for maximum allowed interest     |

  Scenario Outline: Validate API rejects invalid interest rates
    When I send a loan calculation request with
  """
  {
    "currency": "EUR",
    "productType": "SMALL_LOAN_EE01",
    "maturity": 12,
    "administrationFee": 3.99,
    "conclusionFee": 100,
    "amount": 5000,
    "monthlyPaymentDay": 15,
    "interestRate": <interestRate>
  }
  """
    Then the API should return an error for non-numeric amount

    Examples:
      | interestRate | description                |
      | "!!"         | # special char             |
      | "abc"        | # String instead of number |
      | ""           | # Empty interest rate      |


  Scenario Outline: Validate API handles valid administration fees correctly
    When I send a loan calculation request with
  """
  {
    "currency": "EUR",
    "productType": "SMALL_LOAN_EE01",
    "maturity": 12,
    "administrationFee": <administrationFee>,
    "conclusionFee": 100,
    "amount": 5000,
    "monthlyPaymentDay": 15,
    "interestRate": 15.1
  }
  """
    Then the API should return a valid monthly payment and APRC

    Examples:
      | administrationFee |
      | 0                 |
      | 3.99              |
      | 10.00             |
      | 50.50             |
      | 1000.99           |


  Scenario Outline: Validate API rejects invalid administration fees
    When I send a loan calculation request with amount "5000", period "12", interest rate "15.1", and administration fee "<administrationFee>"
    Then the API should return an error for non-numeric amount

    Examples:
      | administrationFee | description                  |
      | "abc"             | # String instead of a number |
      | ""                | # Missing administration fee |

