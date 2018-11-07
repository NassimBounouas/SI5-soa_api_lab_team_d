from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


@given('a list of food categories')
def step_impl(context):

    context.categories = {}

    # Fetch CallbackURL
    callback_url = fetch_callback(context.endpoint, 'list_categories', {})
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

    japanese_exists = False
    context.category = ''

    for c in context.categories:
        if c['name'] == category:
            japanese_exists = True
            context.category = category

    assert japanese_exists is not False


@then('"{meal}" is available at a restaurant')
def step_impl(context, meal):

    meal_exists = False

    form_data = {
        'category': context.category
    }

    # Fetch CallbackURL
    callback_url = fetch_callback(context.endpoint, 'list_meals_by_category', form_data)
    if len(callback_url) == 0:
        context.failed = True
        return

    # Loop until response
    meals = query_callback(callback_url, 'meals')
    for m in meals:
        if str(m['name']).lower() == str(meal).lower():
            meal_exists = True

    assert meal_exists is True
    assert context.failed is False
