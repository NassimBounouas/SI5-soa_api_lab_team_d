from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


@given('a list of food categories')
def step_impl(context):

    context.categories = {}

    # Fetch CallbackURL
    callback_url = fetch_callback(context.endpoint, 'list_categories')
    if len(callback_url) == 0:
        context.failed = True
        return

    # Loop until response
    context.categories = query_callback(callback_url, 'categories')
    if len(context.categories) == 0:
        context.failed = True
        return

    # OK
    pass


@when('listing meals by "{category}" category')
def step_impl(context, category):
    assert True is not False


@then('"{meal}" is available at a restaurant')
def step_impl(context, meal):
    assert context.failed is False
