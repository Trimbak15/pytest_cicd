import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from calculator import add, subtract, multiply, divide

# Link all scenarios in the feature file
scenarios("calculator.feature")

# ── Fixtures (shared state between steps) ──
@pytest.fixture
def context():
    """Holds numbers and result across Given/When/Then."""
    return {}

# ── Given steps ──
@given(parsers.parse('I have the numbers {a:d} and {b:d}'))
def set_numbers(context, a, b):
    context["a"] = a
    context["b"] = b
    context["error"] = None

# ── When steps ──
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

# ── Then steps ──
@then(parsers.parse('the result should be {expected:f}'))
def check_result(context, expected):
    assert context["result"] == expected

@then('a ValueError should be raised')
def check_error(context):
    assert isinstance(context["error"], ValueError) 
    assert "Cannot divide by zero" in str(context["error"])