from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


@given('a steed "{steed_name}" with a GPS position "{lat},{long}"')
def step_impl(context, steed_name, lat, long):
    pass


@when('listing available orders around')
def step_impl(context):
    pass


@then('an order collection is fetched')
def step_impl(context):
    pass
