from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


@given('a restaurant "{restaurant_name}"')
def step_impl(context, restaurant_name):
    pass


@when('creating a new promo code "{promo_pass}" giving a "{promo_discount}" discount')
def step_impl(context, promo_pass, promo_discount):
    pass


@then('customers can use this promo code for reducing the cost of an order')
def step_impl(context):
    pass
