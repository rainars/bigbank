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


  Scenario Outline: Validate API rejects non-numeric values
    When I send a loan calculation request with amount "<amount>" and period "<period>"
    Then the API should return an error for non-numeric amount
#
    Examples:
      | amount | period |
      | "abc"  |  60   |
      | 5000   | "abc" |
      | "abc"  | "abc" |
      | ""     |  60   |
      | 5000   |  ""   |
      | ""     |  ""   |


    Scenario Outline: Validate API rejects negative and zero values
    When I send a loan calculation request with amount "<amount>" and period "<period>"
    Then the API should return an error for invalid loan parameters

    Examples:
      | amount  | period |
      | -5000   |  12    |
      | 5000    | -12    |
      | -5000   | -12    |
      | 0       |  12    |
      | 5000    |  0     |
      | 0       |  0     |

    Scenario Outline: Validate API handles maximum and minimum limits
    When I send a loan calculation request with amount "<amount>" and period "<period>"
    Then the API should return a valid monthly payment and APRC

    Examples:
      | amount  | period |     description       |
      | 100     |  1     |                       |
      | 1000000 |  240   |                       |
      | 5000    |  180   |   Mid-range period    |


    Scenario Outline: Validate API handles decimal values
    When I send a loan calculation request with amount "<amount>" and period "<period>"
    #Then the API should return an error or round appropriately

    Examples:
      | amount   | period |
      | 1000.50  | 12     |
      | 5000.75  | 24     |
      | 99999.99 | 60     |
      | 10000    | 12.5   |
      | 20000.99 | 36     |

    Scenario Outline: Validate API rejects special characters
    When I send a loan calculation request with amount "<amount>" and period "<period>"
    Then the API should return an error for non-numeric amount

    Examples:
      | amount | period |
      | "!!!"  | 12     |
      | 5000   | "@@"   |
      | "###"  | "!!"   |
      | null   | 12     |
     # | 5000   | null   |


