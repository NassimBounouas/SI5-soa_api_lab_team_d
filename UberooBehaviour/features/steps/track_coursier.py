from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


@given('a customer "{customer_name}" with a picked up order id "{order_id}"')
def step_impl(context, customer_name, order_id):
    pass


@when('the customer asks from the geolocation of the coursier')
def step_impl(context):
    pass


@then('the geolocation is returned')
def step_impl(context):
    pass
