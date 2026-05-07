Feature: Calculator operations

  Scenario: Add two numbers
    Given I have the numbers 10 and 5
    When I add them
    Then the result should be 15

  Scenario: Subtract two numbers
    Given I have the numbers 10 and 5
    When I subtract them
    Then the result should be 5

  Scenario: Multiply two numbers
    Given I have the numbers 10 and 5
    When I multiply them
    Then the result should be 50

  Scenario: Divide two numbers
    Given I have the numbers 10 and 5
    When I divide them
    Then the result should be 2

  Scenario: Divide by zero
    Given I have the numbers 10 and 0
    When I divide them
    Then a ValueError should be raised
