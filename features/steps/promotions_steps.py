# pylint: disable=C0114, E302, E0611, C0411, C0116, W3101, E0102
import os
import requests
from behave import given, when, then
from datetime import datetime
from compare3 import expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions


# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_404_NOT_FOUND = 404

WAIT_TIMEOUT = 10

def read_promotion_from_table(row):
    promotion = {
        "promotion_id": int(row["ID"]),
        "promotion_name": row["Name"],
        "promotion_value": int(row["Value"]),
        "promotion_code": row["Code"],
        "promotion_description": row["Description"],
        "promotion_type": row["Type"],
        "active": row["Active"].lower() == "true",
        "promotion_scope": row["Scope"],
        "start_date": datetime.isoformat(datetime.fromisoformat(row["Start Date"])),
        "end_date": datetime.isoformat(datetime.fromisoformat(row["End Date"])),
        "created_by": row["Created By"],
        "modified_by": row["Modified By"],
        "created_when": row["Created When"],
        "modified_when": row["Modified When"]
    }
    return promotion

def to_actual_promotion_id(context, test_promotion_id):
    return str(context.promotions[int(test_promotion_id) - 1])

@given('the server is started')
def step_impl(context):
    context.base_url = os.getenv('BASE_URL', 'http://localhost:8080')
    assert context.resp.status_code == 200


@given('the following promotions')
def step_impl(context):
    # Get a list all of the promotions
    rest_endpoint = f"{context.base_url}/promotions"
    context.resp = requests.get(rest_endpoint, timeout=10)
    expect(context.resp.status_code).equal_to(200)
    # and delete them one by one
    for promotion in context.resp.json():
        context.resp = requests.delete(
            f"{rest_endpoint}/{promotion['promotion_id']}", timeout=WAIT_TIMEOUT
        )
        expect(context.resp.status_code).equal_to(HTTP_204_NO_CONTENT)

    promotions = []
    for row in context.table:
        promotion = read_promotion_from_table(row)
        context.resp = requests.post(rest_endpoint, json=promotion, timeout=WAIT_TIMEOUT)
        print(context.resp.text)
        expect(context.resp.status_code).equal_to(HTTP_201_CREATED)
        id = context.resp.json()["promotion_id"]
        promotions.append(id)
    context.promotions = promotions


@when('I visit the "Home Page"')
def step_impl(context):
    context.base_url = os.getenv('BASE_URL', 'http://localhost:8080')
    context.resp = requests.get(context.base_url + '/')
    context.driver.get(context.base_url + "/")


@when('I look for test promotion id "{test_promotion_id}"')
def step_impl(context, test_promotion_id):
    field = context.driver.find_element(By.ID, "promotion_id")
    actual_promotion_id = to_actual_promotion_id(context, test_promotion_id)
    field.send_keys(actual_promotion_id)

@when('I enter "{fill}" into the "{element_id}" field')
def step_impl(context, fill, element_id):
    field = context.driver.find_element(By.ID, element_id)
    field.send_keys(fill)

@when('I click the "{element_id}" button')
def step_impl(context, element_id):
    button = context.driver.find_element(By.ID, element_id)
    button.click()


@then('I should see "{message}" in the title')
def step_impl(context, message):
    assert message in str(context.resp.text)


@then('I should not see "404 Not Found"')
def step_impl(context):
    assert "404 Not Found" not in str(context.resp.text)

def expect_field_value(context, field_id, expected):
    element = context.driver.find_element(By.ID, field_id)
    value = element.get_attribute("value")
    print("Got", value, "Expected", expected)
    assert value == expected

@then('I should see the promotion details in the form')
def step_impl(context):
    expected_promotion = read_promotion_from_table(context.table[0])
    expected_promotion_id = to_actual_promotion_id(context, expected_promotion["promotion_id"])
    WebDriverWait(context.driver, 3).until(
        expected_conditions.text_to_be_present_in_element_value((By.ID, "promotion_id"), expected_promotion_id)
    )
    expect_field_value(context, "promotion_id", expected_promotion_id)
    expect_field_value(context, "promotion_name", str(expected_promotion["promotion_name"]))
    expect_field_value(context, "promotion_value", str(expected_promotion["promotion_value"]))
    expect_field_value(context, "promotion_code", str(expected_promotion["promotion_code"]))
    expect_field_value(context, "promotion_description", str(expected_promotion["promotion_description"]))
    expect_field_value(context, "promotion_type", str(expected_promotion["promotion_type"]))
    expect_field_value(context, "promotion_scope", str(expected_promotion["promotion_scope"]))
    expect_field_value(context, "start_date", str(expected_promotion["start_date"]))
    expect_field_value(context, "end_date", str(expected_promotion["end_date"]))
    assert True
