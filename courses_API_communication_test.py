# some examples of API communication - course registration tests

import pytest
from playwright.sync_api import sync_playwright

from Data_and_Config.Configuration import *


@pytest.fixture(scope="session")
def api_context():
    playwright = sync_playwright().start()
    request_context = playwright.request.new_context()
    yield request_context
    playwright.stop()


def api_communication(api_context, payload, expected_status):
    headers = { "Content-Type": "application/json" }
    response = api_context.post(URL_REGKURZ_FORM, data=payload, headers=headers)

    print(f"Status: {response.status}")
    print(f"Body: {response.text()}")
    assert response.status == expected_status, f"Expected {expected_status}, got {response.status}\nBody: {response.text()}"
    return response


# ✅ POSITIVE TEST
def test_registration_ok(api_context):
    payload = {
        "targetid": "",
        "kurz": "2",
        "name": "Jan",
        "surname": "Novakščěšíů",
        "email": "jan.novak@abc.cz",
        "phone": "608123123",
        "person": "fyz",
        "address": "Brno",
        "ico": "234563234",
        "count": "1",
        "comment": None,
        "souhlas": True
    }
    api_communication(api_context, payload, 200)


# ❌ NEGATIVE TEST - without course selection
def test_registration_without_course(api_context):
    payload = {
        "targetid": "",
        "kurz": "",
        "name": "Jan",
        "surname": "Novak",
        "email": "jan.novak@abc.cz",
        "phone": "608123123",
        "person": "fyz",
        "address": "Brno",
        "ico": "234563234",
        "count": "1",
        "comment": None,
        "souhlas": True
    }
    api_communication(api_context, payload, 500)


# ❌ NEGATIVE TEST - empty phone number
def test_registration_without_phone(api_context):
    payload = {
        "targetid": "",
        "kurz": "",
        "name": "Jan",
        "surname": "Novak",
        "email": "jan.novak@abc.cz",
        "phone": "",
        "person": "fyz",
        "address": "Brno",
        "ico": "234563234",
        "count": "1",
        "comment": None,
        "souhlas": True
    }
    api_communication(api_context, payload, 500)



# ❌ NEGATIVE TEST - invalid phone number (too long)
def test_registration_invalid_phone(api_context):
    payload = {
        "targetid": "",
        "kurz": "2",
        "name": "Jan",
        "surname": "Novak",
        "email": "jan.novak@abc.cz",
        "phone": "123456789012345",  # number too long
        "person": "fyz",
        "address": "Brno",
        "ico": "234563234",
        "count": "1",
        "comment": None,
        "souhlas": True
    }
    api_communication(api_context, payload, 500)


# ❌ NEGATIVE TEST - invalid email (tohleneniemail.cz)
def test_registration_invalid_email(api_context):
    payload = {
        "targetid": "",
        "kurz": "2",
        "name": "Jan",
        "surname": "Novak",
        "email": "tohleneniemail.cz",
        "phone": "608123123",
        "person": "fyz",
        "address": "Brno",
        "ico": "234563234",
        "count": "1",
        "comment": None,
        "souhlas": True
    }
    api_communication(api_context, payload, 500)


# ❌ NEGATIVE TEST - invalid JSON format (without course key and value, i.e., without "kurz":"2")
def test_registration_invalid_json_format(api_context):
    payload = {
        "targetid": "",
        # "kurz": "2",  # intentionally omitted
        "name": "Jan",
        "surname": "Novak",
        "email": "jan.novak@abc.cz",
        "phone": "608123123",
        "person": "fyz",
        "address": "Brno",
        "ico": "234563234",
        "count": "1",
        "comment": None,
        "souhlas": True
    }
    api_communication(api_context, payload, 500)


# ❌ NEGATIVE TEST - invalid JSON format (unterminated value)
def test_registration_invalid_json_syntax(api_context):
    payload = '''{
        "targetid": "",
        "kurz": "2",
        "name": "Jan",
        "surname": "Novak",
        "email": "jan.novak@abc.cz",
        "phone": "608123123",
        "person": "fyz",
        "address": "Brno",
        "ico": "234563234",
        "count": "1",
        "comment": null,
        "souhlas": true'''  # missing closing brace }
    api_communication(api_context, payload, 500)


# ❌ NEGATIVE TEST - JSON contains special characters, here HTML tag in comment
def test_registration_html_tag(api_context):
    payload = {
        "targetid": "",
        "kurz": "2",
        "name": "Jan",
        "surname": "Novak",
        "email": "jan.novak@abc.cz",
        "phone": "608123123",
        "person": "fyz",
        "address": "Brno",
        "ico": "234563234",
        "count": "1",
        "comment": "<script>alert('test')</script>",  # HTML tag in comment
        "souhlas": True
    }
    api_communication(api_context, payload, 500)