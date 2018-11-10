from behave import *

from share.fetch_callback import fetch_callback
from share.query_callback import query_callback


@given('a steed "{steed_name}"')
def step_impl(context, steed_name):
    pass


@when('computing kpi "{kpi}"')
def step_impl(context, kpi):
    pass


@then('the kpi is returned')
def step_impl(context):
    pass
