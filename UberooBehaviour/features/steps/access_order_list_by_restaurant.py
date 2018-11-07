from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


@given('a restaurant "{restaurant}" with at least two orders')
def step_impl(context, restaurant):

    context.restaurant = {}

    # Fetch CallbackURL
    callback_url = fetch_callback(context.endpoint, 'restaurants', {})
    if len(callback_url) == 0:
        raise ValueError()

    # Loop until response
    restaurants = query_callback(callback_url, 'restaurants')
    if len(restaurants) == 0:
        raise ValueError()

    for r in restaurants:
        if r['name'] == restaurant:
            context.restaurant = r

    if len(context.restaurant) == 0:
        raise ValueError()

    pass


@when('listing dupes for my restaurant')
def step_impl(context):

    context.orders = {}

    form_data = {
        'id_restaurant': context.restaurant['id']
    }

    # Fetch CallbackURL
    callback_url = fetch_callback(context.endpoint, 'order_list_by_restaurant', form_data)
    if len(callback_url) == 0:
        raise ValueError()

    # Loop until response
    context.orders = query_callback(callback_url, 'orders')


@then('an order collection is fetched')
def step_impl(context):

    if len(context.orders) < 2:
        raise ValueError()

    assert len(context.orders) > 2
