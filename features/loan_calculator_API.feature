Feature: Loan Calculator Monthly Payment API

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


#  Scenario Outline: Validate API rejects invalid loan parameters
#    When I send a loan calculation request with amount "<amount>" and period "<period>"
#    Then the API should return an error response
#
#    Examples:
#      | amount | period |
#      | -5000  | 60     |
#      | 5000   | -12    |
#      | -5000  | -12    |