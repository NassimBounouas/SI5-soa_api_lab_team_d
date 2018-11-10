from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


@given('a client "{client_name}" with an order that contains "{meal_name}"')
def step_impl(context, client_name, meal_name):
    pass


@when('leaving a review on meal "{meal_name}"')
def step_impl(context, meal_name):
    pass


@then('the feedback is readable by the chief')
def step_impl(context):
    pass
