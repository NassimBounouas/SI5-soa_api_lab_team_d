from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


@given('a customer "{customer_name}" with an order id "{order_id}"')
def step_impl(context, customer_name, order_id):
    pass


@when('paying with my credit card number "{card_number}", CVV "{cvv}" and expiracy "{expiracy}"')
def step_impl(context, card_number, cvv, expiracy):
    pass


@then('the order is marked as paid')
def step_impl(context):
    pass
