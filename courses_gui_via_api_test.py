"""
GUI tests via API for course registration form simulated as a GUI interaction, where inputs are entered as in a form

"""

import pytest
from playwright.sync_api import sync_playwright
import os
import json

from Data_and_Config.Configuration import *


@pytest.fixture(scope="session")
def api_context():
    playwright = sync_playwright().start()
    context = playwright.request.new_context()
    yield context
    playwright.stop()


def send_registration(
    api_context, course, name, surname, email, phone, person, count, comment, consent, expected_status, **kwargs
):

    if person == "fyz":
        address = kwargs.get("address")
        if not address:
            raise AssertionError("The 'address' field is required for a fyz person.")
    elif person == "pra":
        ico = kwargs.get("ico")
        if not ico:
            raise AssertionError("The 'ico' field is required for a pra person.")
    else:
        raise AssertionError("The 'person' value must be either 'fyz' or 'pra'.")

    payload = {
        "targetid": "",
        "kurz": course,
        "name": name,
        "surname": surname,
        "email": email,
        "phone": phone,
        "person": person,
        "count": count,
        "comment": comment,
        "souhlas": consent,
    }

    if person == "fyz":
        payload["address"] = address
    if person == "pra":
        payload["ico"] = ico

    test_name = os.environ.get("PYTEST_CURRENT_TEST", "<unknown>").split(" ")[0]
    print(f"\n>>> {test_name}: \nPayload: {json.dumps(payload, indent=2, ensure_ascii=False)}")

    # print(f"Payload: {payload}")

    # headers = { "Content-Type": "application/json" }
    response = api_context.post(URL_REGKURZ_FORM, data=payload)  # , headers=headers)

    print(f"\nResponse:")
    print(f"Status: {response.status}")
    print(f"Body: {response.text()}")
    assert (
        response.status == expected_status
    ), f"Expected {expected_status}, got {response.status}\nBody: {response.text()}"
    return response


# --- TEST CASES ---


# ✅ POSITIVE TEST - with person type fyz
def test_registration_fyz_success(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="Jan",
        surname="Novakščěšíů",
        email="jan.novak@abc.cz",
        phone="608123123",
        person="fyz",
        address="Brno",
        count="1",
        comment=None,
        consent=True,
        expected_status=200,
    )


# ✅ POSITIVE TEST - with person type pra
def test_registration_pra_success(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="Jan",
        surname="Novakščěšíů",
        email="jan.novak@abc.cz",
        phone="608123123",
        person="pra",
        ico="25596641",
        count="1",
        comment=None,
        consent=True,
        expected_status=200,
    )


# ❌ NEGATIVE TEST - without course selection
def test_registration_without_course(api_context):
    send_registration(
        api_context=api_context,
        course="",
        name="Jan",
        surname="Novak",
        email="jan.novak@abc.cz",
        phone="608123123",
        person="fyz",
        address="Brno",
        count="1",
        comment=None,
        consent=True,
        expected_status=500,
    )


# ❌ NEGATIVE TEST - empty phone number
def test_registration_without_phone(api_context):
    send_registration(
        api_context=api_context,
        course="",
        name="Jan",
        surname="Novak",
        email="jan.novak@abc.cz",
        phone="",
        person="fyz",
        address="Brno",
        count="1",
        comment=None,
        consent=True,
        expected_status=500,
    )


# ❌ NEGATIVE TEST - invalid phone number (too long)
def test_registration_invalid_phone(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="Jan",
        surname="Novak",
        email="jan.novak@abc.cz",
        phone="123456789012345",
        person="fyz",
        address="Brno",
        count="1",
        comment=None,
        consent=True,
        expected_status=500,
    )


# ❌ NEGATIVE TEST - invalid email
def test_registration_invalid_email(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="Jan",
        surname="Novak",
        email="tohleneniemail",
        phone="608123123",
        person="fyz",
        address="Brno",
        count="1",
        comment=None,
        consent=True,
        expected_status=500,
    )


# ✅ POSITIVE TEST - system handles very long surname
def test_registration_handles_long_surname(api_context):
    very_long_surname = "X" * 100
    send_registration(
        api_context=api_context,
        course="2",
        name="Jan",
        surname=very_long_surname,
        email="jan.novak@abc.cz",
        phone="608123123",
        person="fyz",
        address="Brno",
        count="1",
        comment=None,
        consent=True,
        expected_status=200,
    )


# --- Additional Test Cases ---

# Email Validation Tests


# ✅ POSITIVE TEST - email with multiple subdomains is accepted
def test_valid_email_with_subdomains(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="Alice",
        surname="Smith",
        email="alice.smith@sub.company.co.uk",
        phone="608123123",
        person="fyz",
        address="Prague",
        count="1",
        comment=None,
        consent=True,
        expected_status=200,
    )


# ✅ POSITIVE TEST - email with plus sign (Gmail style) is valid
def test_valid_email_with_plus_sign(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="Bob",
        surname="Jones",
        email="bob+course@example.com",
        phone="608123123",
        person="fyz",
        address="Ostrava",
        count="1",
        comment=None,
        consent=True,
        expected_status=200,
    )


# ❌ NEGATIVE TEST - email without @ symbol is rejected
def test_invalid_email_missing_at_symbol(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="John",
        surname="Doe",
        email="johndoeexample.com",
        phone="608123123",
        person="fyz",
        address="Brno",
        count="1",
        comment=None,
        consent=True,
        expected_status=500,
    )


# ❌ NEGATIVE TEST - email without domain part is rejected
def test_invalid_email_missing_domain(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="Jane",
        surname="Wilson",
        email="jane@",
        phone="608123123",
        person="fyz",
        address="Brno",
        count="1",
        comment=None,
        consent=True,
        expected_status=500,
    )


# Phone Number Validation Tests


# ✅ POSITIVE TEST - phone number with country code (+420) is accepted
def test_valid_phone_with_country_code(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="Martin",
        surname="Brown",
        email="martin@test.cz",
        phone="+420608123123",
        person="fyz",
        address="Plzen",
        count="1",
        comment=None,
        consent=True,
        expected_status=200,
    )


# ❌ NEGATIVE TEST - phone number with insufficient digits is rejected
def test_invalid_phone_too_short(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="Eva",
        surname="Black",
        email="eva@test.cz",
        phone="12345",
        person="fyz",
        address="Brno",
        count="1",
        comment=None,
        consent=True,
        expected_status=500,
    )


# ❌ NEGATIVE TEST - phone number containing letters is rejected
def test_invalid_phone_with_letters(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="Pavel",
        surname="Green",
        email="pavel@test.cz",
        phone="608ABC123",
        person="fyz",
        address="Praha",
        count="1",
        comment=None,
        consent=True,
        expected_status=500,
    )


# Name and Surname Validation Tests


# ✅ POSITIVE TEST - server accepts numeric-only name (boundary case)
def test_valid_name_numbers_only(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="12345",
        surname="Valid",
        email="test@test.cz",
        phone="608123123",
        person="fyz",
        address="Brno",
        count="1",
        comment=None,
        consent=True,
        expected_status=200,
    )


# ❌ NEGATIVE TEST - empty surname field is rejected
def test_invalid_empty_surname(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="John",
        surname="",
        email="test@test.cz",
        phone="608123123",
        person="fyz",
        address="Brno",
        count="1",
        comment=None,
        consent=True,
        expected_status=500,
    )


# ✅ POSITIVE TEST - name with Czech special characters is accepted
def test_valid_name_with_special_characters(api_context):
    send_registration(
        api_context=api_context,
        course="2",
        name="Jiří",
        surname="Dvořák",
        email="test@test.cz",
        phone="608123123",
        person="fyz",
        address="Brno",
        count="1",
        comment=None,
        consent=True,
        expected_status=200,
    )


# Combined and Edge Cases


# ❌ NEGATIVE TEST - legal entity (pra) without ICO raises AssertionError
def test_pra_invalid_missing_ico(api_context):
    with pytest.raises(AssertionError) as excinfo:
        send_registration(
            api_context=api_context,
            course="2",
            name="Company",
            surname="Ltd",
            email="company@test.cz",
            phone="608123123",
            person="pra",
            ico="",
            count="1",
            comment=None,
            consent=True,
            expected_status=500,
        )
    assert str(excinfo.value) == "The 'ico' field is required for a pra person."


# ❌ NEGATIVE TEST - natural person (fyz) without address raises AssertionError
def test_fyz_invalid_missing_address(api_context):
    with pytest.raises(AssertionError) as excinfo:
        send_registration(
            api_context=api_context,
            course="2",
            name="John",
            surname="Smith",
            email="john@test.cz",
            phone="608123123",
            person="fyz",
            address="",
            count="1",
            comment=None,
            consent=True,
            expected_status=500,
        )
    assert str(excinfo.value) == "The 'address' field is required for a fyz person."
