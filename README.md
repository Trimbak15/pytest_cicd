# Yaml corrected code 

name: pytest CI

on:
  push:
    branches: [ main ]

  pull_request:
    branches: [ main ]

jobs:
  test:

    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:

      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-html

      - name: Create reports directory
        run: mkdir -p reports

      - name: Run pytest
        run: |
          pytest -v \
            --cov=calculator \
            --cov-report=xml \
            --cov-fail-under=80 \
            --html=reports/report.html \
            --self-contained-html

      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-report-py${{ matrix.python-version }}
          path: reports/



  # calculator.feature (gharkins) 

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


# test_calculator_bdd.py

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from calculator import add, subtract, multiply, divide

scenarios("calculator.feature")

# Given steps
@given(parsers.parse('I have the numbers {a:d} and {b:d}'), target_fixture="context")
def set_numbers(a, b):
    return {"a": a, "b": b, "error": None, "result": None}

# When steps
@when('I add them')
def when_add(context):
    context["result"] = add(context["a"], context["b"])

@when('I subtract them')
def when_subtract(context):
    context["result"] = subtract(context["a"], context["b"])

@when('I multiply them')
def when_multiply(context):
    context["result"] = multiply(context["a"], context["b"])

@when('I divide them')
def when_divide(context):
    try:
        context["result"] = divide(context["a"], context["b"])
    except ValueError as e:
        context["error"] = e

# Then steps
@then(parsers.parse('the result should be {expected:g}'))
def check_result(context, expected):
    assert context["result"] == pytest.approx(expected)

@then('a ValueError should be raised')
def check_error(context):
    assert isinstance(context["error"], ValueError)
    assert "Cannot divide by zero" in str(context["error"])
