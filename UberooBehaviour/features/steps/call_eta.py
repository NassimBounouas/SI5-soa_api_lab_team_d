from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


@given('a customer "{customer_name}" with an order "{order_id}"')
def step_impl(context, customer_name, order_id):
    pass


@when('calling the ETA service for my order')
def step_impl(context):
    pass


@then('an estimated time of arrival is provided')
def step_impl(context):
    pass
