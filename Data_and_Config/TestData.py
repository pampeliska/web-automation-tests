#
# This file contains all Test Data
#

# User
USER1_EMAIL = "giyipem264@v1zw.com"
USER1_PASSWORD = "tajnenovak"
EMPTY = ""
LONG_INVALID_EMAIL = "a" * 100 + "@email.com"
SPECIAL_CHARS_PASSWORD = "' OR '1'='1"
MALICIOUS_EMAIL = "<script>alert('XSS')</script>@email.com"

# Strings
TITLE_COURSES = "Testování - Přehled kurzů"
TITLE_FORGOT_PASSWORD = "Testování - zapomenuté heslo"
TEXT_LOGIN_LINK = "Přihlásit se"
TEXT_LOGOUT_BUTTON = "Odhlásit se"

# Validation error messages
ERROR_NAME_REQUIRED = "The name field is required."
ERROR_EMAIL_REQUIRED = "The email field is required."
ERROR_PASSWORD_REQUIRED = "The password field is required."
ERROR_EMAIL_TAKEN = "The email has already been taken."
ERROR_PASSWORD_CONFIRMATION = "The password field confirmation does not match."
ERROR_USER_NOT_FOUND = "We can't find a user with that email address."
ERROR_EMAIL_SHOULD_NOT_CONTAIN = "A part followed by '@' should not contain"
ERROR_EMAIL_MISSING_AT = "Please include an '@' in the email address."
ERROR_INVALID_CREDENTIALS = "These credentials do not match our records."

# Status messages and others
STATUS_PASSWORD_RESET_SENT = "We have emailed your password reset link."
WELCOME_USER = "Vítej uživateli {fake_name}!"

# Logging messages
PRINT_LOGGING_IN_USER = "Logging in user: {email} with password: {password}"
PRINT_REGISTERING_USER = "Registering user: {fake_name}, email: {fake_email}, password: {fake_password}"
PRINT_USER_LOGGED_OUT = "User logged out"

# Locators (data-test attributes)
# Header locators
LOCATOR_LOGIN_LINK = "[data-test=login_link]"
LOCATOR_LOGOUT_BUTTON = "[data-test=logout_button]"

# Login, Registration and Forgot Password locators
LOCATOR_REGISTER_LINK = "[data-test=register_link]"
LOCATOR_FORGOT_PASSWORD_LINK = "[data-test=forgot_password_link]"
LOCATOR_EMAIL_INPUT = "[data-test=email_input]"
LOCATOR_PASSWORD_INPUT = "[data-test=password_input]"
LOCATOR_LOGIN_BUTTON = "[data-test=login_button]"
LOCATOR_NAME_INPUT = "[data-test=name_input]"
LOCATOR_PASSWORD_AGAIN_INPUT = "[data-test=password_again_input]"
LOCATOR_REGISTER_BUTTON = "[data-test=register_button]"
LOCATOR_HOME_SECTION = "[data-test=home_section]"
LOCATOR_NAME_INPUT_ERRORS = "[data-test=name_input_errors]"
LOCATOR_EMAIL_INPUT_ERRORS = "[data-test=email_input_errors]"
LOCATOR_EMAIL_INPUT_ERRORS_DIV = "[data-test=email_input_errors_div]"
LOCATOR_PASSWORD_INPUT_ERRORS = "[data-test=password_input_errors]"
LOCATOR_SUBMIT_BUTTON = "[data-test=submit_button]"
LOCATOR_STATUS_DIV = "[data-test=status_div]"
