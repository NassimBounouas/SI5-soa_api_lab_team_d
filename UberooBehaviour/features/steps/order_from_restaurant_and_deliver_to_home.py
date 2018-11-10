from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


# Scenario: Order a lunch from a restaurant

@given('a client "{customer_name}" that wants to eat "{meal_name}"')
def step_impl(context, customer_name, meal_name):
    pass


@when('the order is marked as ready for pickup')
def step_impl(context):
    pass


@then('the order is available for pickup by steeds')
def step_impl(context):
    pass


########################################################################################################################


# Scenario: Deliver a lunch to a place

@given('a client "{customer_name}" and its last order ready for pickup')
def step_impl(context, customer_name):
    pass


@when('the order is to customer place')
def step_impl(context):
    pass


@then('the order is marked as delivered')
def step_impl(context):
    pass
