"""
Some E2E tests for course registration

"""

import pytest
from faker import Faker
from playwright.sync_api import expect

from Data_and_Config.TestData import *
from Data_and_Config.Configuration import *

# Fixtures


@pytest.fixture(scope="function")
def fake():
    return Faker("cs_CZ")


# Fixture that ensures opening the courses page before the test
# and attempts to log out the user after the test (if logged in)
@pytest.fixture(scope="function")
def _setup_and_teardown_login(page):
    page.set_default_timeout(TIMEOUT_BROWSER)
    page.goto(URL_COURSES)
    expect(page).to_have_title(TITLE_COURSES)
    yield  # page is not returned, page is a separate fixture in tests
    try:
        logout(page)
    except Exception:
        # If not logged in/cannot click, skip the error
        pass


# Helper functions


def login_with_verification(page, email, password, should_be_logged_in):

    login_without_verification(page, email, password)
    if should_be_logged_in:
        verify_user_is_logged_in(page)
    else:
        verify_user_is_not_logged_in(page)


def login_without_verification(page, email, password):
    # page.pause()
    print(PRINT_LOGGING_IN_USER.format(email=email, password=password))
    page.click(LOCATOR_LOGIN_LINK)
    page.fill(LOCATOR_EMAIL_INPUT, email)
    page.fill(LOCATOR_PASSWORD_INPUT, password)
    page.click(LOCATOR_LOGIN_BUTTON)


def verify_user_is_logged_in(page):
    expect(page.locator(LOCATOR_LOGOUT_BUTTON).first).to_have_text(TEXT_LOGOUT_BUTTON)


def verify_user_is_not_logged_in(page):
    expect(page.locator(LOCATOR_LOGIN_LINK).first).to_have_text(TEXT_LOGIN_LINK)


def logout(page):
    page.locator(LOCATOR_LOGOUT_BUTTON).click()
    print("User logged out")
    verify_user_is_not_logged_in(page)


def open_login_page(page):
    page.locator(LOCATOR_LOGIN_LINK).click()


def open_registration_page(page):
    open_login_page(page)
    page.locator(LOCATOR_REGISTER_LINK).click()


def open_forgot_password_page(page):
    open_registration_page(page)
    page.locator(LOCATOR_FORGOT_PASSWORD_LINK).click()


def register_user(page, fake):
    fake_name = fake.first_name()
    fake_email = fake.unique.email()
    fake_password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    print(PRINT_REGISTERING_USER.format(fake_name=fake_name, fake_email=fake_email, fake_password=fake_password))
    open_registration_page(page)
    page.fill(LOCATOR_NAME_INPUT, fake_name)
    page.fill(LOCATOR_EMAIL_INPUT, fake_email)
    page.fill(LOCATOR_PASSWORD_INPUT, fake_password)
    page.fill(LOCATOR_PASSWORD_AGAIN_INPUT, fake_password)
    page.click(LOCATOR_REGISTER_BUTTON)
    expect(page.locator(LOCATOR_LOGOUT_BUTTON)).to_have_text(TEXT_LOGOUT_BUTTON)
    expect(page.locator(LOCATOR_HOME_SECTION)).to_contain_text(WELCOME_USER.format(fake_name=fake_name))
    expect(page).to_have_url(URL_HOME)

    return fake_email, fake_password, fake_name


# Tests


def test_login_invalid_email(page, _setup_and_teardown_login):
    login_with_verification(page, "dsadsad@sdas.cz", "dasdas", False)
    expect(page.locator(LOCATOR_EMAIL_INPUT_ERRORS)).to_have_text(ERROR_INVALID_CREDENTIALS)
    print("✅ test_login_invalid_email completed")


def test_login_invalid_password(page, _setup_and_teardown_login):
    login_with_verification(page, "janca.tester@seznam.cz", "dasdas", False)
    expect(page.locator(LOCATOR_EMAIL_INPUT_ERRORS)).to_have_text(ERROR_INVALID_CREDENTIALS)
    print("✅ test_login_invalid_password completed")


def test_login_long_invalid_password(page, _setup_and_teardown_login):
    login_with_verification(page, "janca.tester@seznam.cz", "d" * 100, False)
    expect(page.locator(LOCATOR_EMAIL_INPUT_ERRORS)).to_have_text(ERROR_INVALID_CREDENTIALS)
    print("✅ test_login_long_invalid_password completed")


def test_login_long_invalid_email(page, _setup_and_teardown_login):
    login_with_verification(page, LONG_INVALID_EMAIL, USER1_PASSWORD, False)
    expect(page.locator(LOCATOR_EMAIL_INPUT_ERRORS)).to_have_text(ERROR_INVALID_CREDENTIALS)
    print("✅ test_login_long_invalid_email completed")


def test_login_script_injection_email(page, _setup_and_teardown_login):
    login_with_verification(page, MALICIOUS_EMAIL, "hesloheslo", False)
    validation_message = page.locator(LOCATOR_EMAIL_INPUT).evaluate("e => e.validationMessage")

    assert ERROR_EMAIL_SHOULD_NOT_CONTAIN in validation_message
    print("✅ test_login_script_injection_email completed")


def test_login_special_chars_password(page, _setup_and_teardown_login):
    login_with_verification(page, USER1_EMAIL, SPECIAL_CHARS_PASSWORD, False)
    expect(page.locator(LOCATOR_EMAIL_INPUT_ERRORS)).to_have_text(ERROR_INVALID_CREDENTIALS)
    print("✅ test_login_special_chars_password completed")


def test_login_empty_credentials(page, _setup_and_teardown_login):
    login_with_verification(page, EMPTY, EMPTY, False)
    expect(page.locator(LOCATOR_EMAIL_INPUT_ERRORS)).to_have_text(ERROR_EMAIL_REQUIRED)
    expect(page.locator(LOCATOR_PASSWORD_INPUT_ERRORS)).to_have_text(ERROR_PASSWORD_REQUIRED)
    print("✅ test_login_empty_credentials completed")


def test_login_empty_email(page, _setup_and_teardown_login):
    login_with_verification(page, EMPTY, USER1_PASSWORD, False)
    expect(page.locator(LOCATOR_EMAIL_INPUT_ERRORS)).to_have_text(ERROR_EMAIL_REQUIRED)
    print("✅ test_login_empty_email completed")


def test_login_empty_password(page, _setup_and_teardown_login):
    login_with_verification(page, USER1_EMAIL, EMPTY, False)
    expect(page.locator(LOCATOR_PASSWORD_INPUT_ERRORS)).to_have_text(ERROR_PASSWORD_REQUIRED)
    print("✅ test_login_empty_password completed")


def test_login_success(page, _setup_and_teardown_login):
    login_with_verification(page, USER1_EMAIL, USER1_PASSWORD, True)
    print("✅ test_login_success completed")


def test_login_success_with_external_verification(page, _setup_and_teardown_login):
    login_without_verification(page, USER1_EMAIL, USER1_PASSWORD)
    verify_user_is_logged_in(page)
    print("✅ test_login_success_with_external_verification completed")


# verify that user is logged in with new credentials,
# logout and re-login with new credentials and verify that user is logged in
def test_registration_success(page, fake, _setup_and_teardown_login):
    email, password, name = register_user(page, fake)
    logout(page)

    # Re-login with new credentials
    login_with_verification(page, email, password, True)
    print("✅ test_registration_success completed")


def test_registration_empty_fields(page, _setup_and_teardown_login):
    open_registration_page(page)
    page.click(LOCATOR_REGISTER_BUTTON)
    expect(page.locator(LOCATOR_NAME_INPUT_ERRORS)).to_have_text(ERROR_NAME_REQUIRED)
    expect(page.locator(LOCATOR_EMAIL_INPUT_ERRORS)).to_have_text(ERROR_EMAIL_REQUIRED)
    expect(page.locator(LOCATOR_PASSWORD_INPUT_ERRORS)).to_have_text(ERROR_PASSWORD_REQUIRED)
    verify_user_is_not_logged_in(page)
    print("✅ test_registration_empty_fields completed")


def test_registration_existing_email(page, fake, _setup_and_teardown_login):

    # First registration - successful
    email, password, name = register_user(page, fake)
    logout(page)

    # Second registration with the same email - expecting error
    open_registration_page(page)
    page.fill(LOCATOR_NAME_INPUT, name)
    page.fill(LOCATOR_EMAIL_INPUT, email)
    page.fill(LOCATOR_PASSWORD_INPUT, password)
    page.fill(LOCATOR_PASSWORD_AGAIN_INPUT, password)
    page.click(LOCATOR_REGISTER_BUTTON)
    expect(page.locator(LOCATOR_EMAIL_INPUT_ERRORS)).to_have_text(ERROR_EMAIL_TAKEN)
    verify_user_is_not_logged_in(page)
    print("✅ test_registration_existing_email completed")


def test_registration_invalid_email_format(page, _setup_and_teardown_login):
    name = "Test"
    invalid_email = "emailwithoutatsign"
    password = "12345678"
    open_registration_page(page)
    page.fill(LOCATOR_NAME_INPUT, name)
    page.fill(LOCATOR_EMAIL_INPUT, invalid_email)
    page.fill(LOCATOR_PASSWORD_INPUT, password)
    page.fill(LOCATOR_PASSWORD_AGAIN_INPUT, password)
    page.click(LOCATOR_REGISTER_BUTTON)

    # Verification of field validation - JavaScript function via Python Playwright
    # for HTML5 validation of browser email field - system element rendered above the page
    # and is not part of the page's DOM
    validation_message = page.locator(LOCATOR_EMAIL_INPUT).evaluate("e => e.validationMessage")
    # assert only on part of the text
    assert ERROR_EMAIL_MISSING_AT in validation_message

    verify_user_is_not_logged_in(page)
    print("✅ test_registration_invalid_email_format completed")


def test_registration_password_mismatch(page, _setup_and_teardown_login):
    name = "Test"
    email = "testovy.email@example.com"
    password = "SpravneHeslo"
    password_mismatch = "JineHeslo"

    open_registration_page(page)
    page.fill(LOCATOR_NAME_INPUT, name)
    page.fill(LOCATOR_EMAIL_INPUT, email)
    page.fill(LOCATOR_PASSWORD_INPUT, password)
    page.fill(LOCATOR_PASSWORD_AGAIN_INPUT, password_mismatch)
    page.click(LOCATOR_REGISTER_BUTTON)
    expect(page.locator(LOCATOR_PASSWORD_INPUT_ERRORS)).to_have_text(ERROR_PASSWORD_CONFIRMATION)

    verify_user_is_not_logged_in(page)
    print("✅ test_registration_password_mismatch completed")


def test_forgot_password_success(page, _setup_and_teardown_login):
    email = "rostislavjelinek@example.com"  # registered email

    open_forgot_password_page(page)
    # page.goto(URL_FORGOT_PASSWORD)

    expect(page).to_have_title(TITLE_FORGOT_PASSWORD)
    page.fill(LOCATOR_EMAIL_INPUT, email)
    page.click(LOCATOR_SUBMIT_BUTTON)

    expect(page.locator(LOCATOR_STATUS_DIV)).to_have_text(STATUS_PASSWORD_RESET_SENT)
    print("✅ test_forgot_password_success completed")


# @pytest.mark.skip
def test_forgot_password_nonexistent_email(page, _setup_and_teardown_login):
    nonexistent_email = "jancin_neznamy@email.cz"

    open_forgot_password_page(page)
    expect(page).to_have_title(TITLE_FORGOT_PASSWORD)
    page.fill(LOCATOR_EMAIL_INPUT, nonexistent_email)
    page.click(LOCATOR_SUBMIT_BUTTON)

    expect(page.locator(LOCATOR_EMAIL_INPUT_ERRORS)).to_have_text(ERROR_USER_NOT_FOUND)
    print("✅ test_forgot_password_nonexistent_email completed")
