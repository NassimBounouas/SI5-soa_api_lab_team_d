from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


# Scenario: Order a lunch from a restaurant

@given('a customer "{customer_name}" that wants to eat "{meal_name}" at "{client_address}"')
def step_impl(context, customer_name, meal_name, client_address):
    context.customer_name = customer_name
    context.meal_name = meal_name
    context.client_address = client_address


@when('"{customer_name}" is browsing the menu correspoding to the category "{category_name}" and he selects "{meal_name}"')
def step_impl(context, customer_name, category_name, meal_name):

    # Fetch CallbackURL
    callback_url = fetch_callback(context.endpoint, 'list_meals_by_category', {"category": category_name})
    if len(callback_url) == 0:
        raise ValueError()

    # Loop until response
    context.meals = query_callback(callback_url, 'meals')
    if len(context.meals) == 0:
        raise ValueError()

    for meal in context.meals:
        if meal["name"] == meal_name:
            context.meal = meal


@then('"{customer_name}" is ordering the meal from the right restaurant to be delivered at "{client_address}"')
def step_impl(context, customer_name, client_address):

    # Fetch CallbackURL
    callback_url = fetch_callback(context.endpoint, 'order', {"id_restaurant": context.meal["restaurant"]["id"],
                                                              "id_meal": context.meal["id"],
                                                              "client_name": customer_name,
                                                              "client_address": client_address})
    if len(callback_url) == 0:
        raise ValueError()

    # Loop until response
    context.order = query_callback(callback_url, 'order')
    if context.order["status"] != 'Created':
        raise ValueError()


@then('A delivery request is created')
def step_impl(context):

    # Fetch CallbackURL
    callback_url = fetch_callback(context.endpoint, 'order_list_by_restaurant', {"id_restaurant": context.order["id_restaurant"]})
    if len(callback_url) == 0:
        raise ValueError()

    # Loop until response
    order_list = query_callback(callback_url, 'List')
    found = False
    for order in order_list:
        if order["id_order"] != context.order["id_order"]:
            found = True
            break

    if not found:
        raise ValueError()
    pass
