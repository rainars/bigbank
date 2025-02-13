Feature: Loan Calculator Monthly Payment

  Scenario Outline: Customer must be able to choose their loan amount and loan period.
    Given the loan calculator page is opened
    When I set the loan amount to "<amount>"
    And I set the loan period to "<period>"
    Then the monthly payment should not be "€0"

    Examples:
      | amount   | period |
      | 30000.99 | 6      |
      | 30000    | 6      |
      | 30000    | 12     |
      | 30000    | 24     |
      | 30000    | 36     |
      | 30000    | 48     |
      | 30000    | 60     |
      | 30000    | 120    |
      | 500      | 6      |
      | 500      | 12     |
      | 500      | 24     |
      | 500      | 36     |
      | 500      | 48     |
      | 500      | 60     |
      | 500      | 120    |

  Scenario Outline: Edge cases - Verify modal accepts only positive number values
    Given the loan calculator page is opened
    When I set the loan amount to "<amount>"
    And I set the loan period to "<period>"
    Then the monthly payment should not be "€0"

    Examples:
      | amount | period |
      | 30000  | -6     |
      | -30000 | 12     |
      | -30000 | -48    |
      | "abc"  | 24     |
      | 30000  | "abc"  |
      | "abc"  | 48     |
      | "abc"  | "abc"  |

  Scenario: Verify loan calculation via API and UI consistency
    Given the loan calculator page is opened
    When I set the loan amount to "5000"
    And I set the loan period to "60"
    And I send a loan calculation request with amount "5000" and period "60"
    Then the API should return a valid monthly payment and APRC
    And the calculated monthly payment should match the API result

  Scenario Outline: Validate loan calculations for different values
    When I send a loan calculation request with amount "<amount>" and period "<period>"
    Then the API should return a valid monthly payment and APRC

    Examples:
      | amount | period |
      | 1000   | 12     |
      | 2000   | 24     |
      | 5000   | 36     |
      | 10000  | 48     |
      | 20000  | 60     |

  Scenario Outline: Validate API rejects invalid loan parameters
    When I send a loan calculation request with amount "<amount>" and period "<period>"
    Then the API should return an error response

    Examples:
      | amount | period |
      | -5000  | 60     |
      | 5000   | -12    |
      | -5000  | -12    |

  Scenario Outline: Calculator changes should not be saved before clicking the save button
    Given the loan calculator page is opened
    When I set the loan amount to "<amount>"
    And I set the loan period to "<period>"
    And I close the loan calculator without saving
    And I reopen the loan calculator
    Then the loan amount should be the default value
    And the loan period should be the default value
    When I set the loan amount to "<amount>"
    And I set the loan period to "<period>"
    And I click the save button
    And I reopen the loan calculator
    Then the loan amount "<amount>" should persist after saving

    Examples:
      | amount | period | expected_amount |
      | 10000  | 36     | 10000           |
      | 30000  | 16     | 30000           |

  Scenario Outline: Validate extreme values for loan calculation
    When I send a loan calculation request with amount "<amount>" and period "<period>"
    Then the API should return a valid monthly payment and APRC

    Examples:
      | amount | period |
      | 1      | 12     |
      | 999999 | 120    |
      | 5000   | 1      |
      | 5000   | 360    |
      | 5000   | 60     |
