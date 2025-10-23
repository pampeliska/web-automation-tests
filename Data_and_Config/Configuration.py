#
# This file contains all configuration parameters and variables
#

URL_BASE = "http://testovani.kitner.cz"
URL_COURSES = f"{URL_BASE}/courses"
URL_HOME = f"{URL_BASE}/home"
URL_FORGOT_PASSWORD = f"{URL_BASE}/forgot-password"
URL_REGKURZ_FORM = f"{URL_BASE}/regkurz/formsave.php"

PORT = 80

# Time between clicks and checks in milliseconds
TIME_BETWEEN_CLICKS = 100  # 100 ms
TIME_BETWEEN_CHECKS = 200  # 200 ms

# Timeouts
TIMEOUT_BROWSER = 3000  # 10000  # in milliseconds (3 s)
TC_TIMEOUT_PW_KW = 20 * 60 * 1000  # 20 minutes
