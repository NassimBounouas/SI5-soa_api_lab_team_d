from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


@given('an order "{order_id}" being delivered by "{steed_name}"')
def step_impl(context, order_id, steed_name):
    pass


@when('the steed notify that an issue preventing the delivery happened')
def step_impl(context):
    pass


@then('the order is rescheduled')
def step_impl(context):
    pass
