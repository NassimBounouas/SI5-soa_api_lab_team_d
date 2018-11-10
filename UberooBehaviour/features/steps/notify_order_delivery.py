from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


@given('a steed "{steed_name}" with a delivered order id "{order_id}"')
def step_impl(context, steed_name, order_id):
    pass


@when('sending notification message of a successful delivery')
def step_impl(context):
    pass


@then('an order is marked as delivered')
def step_impl(context):
    pass
