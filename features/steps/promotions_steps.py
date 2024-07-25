# pylint: disable=C0114, E302, E0611, C0411, C0116, W3101, E0102
import os
import requests
from behave import given, when, then
from datetime import datetime


@given('the server is started')
def step_impl(context):
    context.base_url = os.getenv('BASE_URL', 'http://localhost:8080')
    assert context.resp.status_code == 200


@given('the following promotions')
def step_impl(context):
    promotions = []
    for row in context.table:
        promotion = {
            "id": int(row["ID"]),
            "name": row["Name"],
            "value": int(row["Value"]),
            "code": row["Code"],
            "description": row["Description"],
            "type": row["Type"],
            "active": row["Active"].lower() == "true",
            "scope": row["Scope"],
            "start_date": datetime.strptime(row["Start Date"], "%Y-%m-%d"),
            "end_date": datetime.strptime(row["End Date"], "%Y-%m-%d"),
            "created_by": row["Created By"],
            "modified_by": row["Modified By"],
            "created_when": datetime.strptime(row["Created When"], "%Y-%m-%d"),
            "modified_when": datetime.strptime(row["Modified When"], "%Y-%m-%d"),
        }
        promotions.append(promotion)
    context.promotions = promotions


@when('I visit the "Home Page"')
def step_impl(context):
    context.base_url = os.getenv('BASE_URL', 'http://localhost:8080')
    context.resp = requests.get(context.base_url + '/')
    assert context.resp.status_code == 200


@then('I should see "{message}" in the title')
def step_impl(context, message):
    assert message in str(context.resp.text)


@then('I should not see "404 Not Found"')
def step_impl(context):
    assert "404 Not Found" not in str(context.resp.text)