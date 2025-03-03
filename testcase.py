from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# ==== Safari WebDriver Setup (Default) ====
driver = webdriver.Safari()  # Safari does not need WebDriver Manager

"""
# ==== Chrome WebDriver Setup (Commented) ====
# Uncomment the lines below if using Chrome, and comment out the Safari line above.

# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options

# options = Options()
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=options)
"""

try:
    # ----------------------------------------------------------------------------
    # Test Case 1: Multiple Invalid Login Attempts
    # (Trying different invalid inputs in one case)
    # ----------------------------------------------------------------------------
    print("\n🔹 Test Case 1: Multiple Invalid Login Attempts")
    driver.get("http://127.0.0.1:5000/")
    driver.maximize_window()
    time.sleep(1)

    invalid_combos = [
        ("invalid@example.com", "wrongpassword"),
        ("user@example.com",   "wrongpassword"),  # valid user but wrong pass
        ("random@random.com",  "random123")
    ]

    all_invalid_passed = True
    for (test_user, test_pass) in invalid_combos:
        # Enter credentials
        username_input = driver.find_element(By.NAME, "username")
        username_input.clear()
        username_input.send_keys(test_user)

        password_input = driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(test_pass)

        # Click login
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        time.sleep(2)

        # Check for error message
        try:
            error_message = driver.find_element(By.XPATH, "//p[@style='color: red;']")
            if "Invalid" in error_message.text:
                print(f"   ✅ Invalid login test PASSED for {test_user}/{test_pass}")
            else:
                print(f"   ❌ Invalid login test FAILED (no 'Invalid' text) for {test_user}/{test_pass}")
                all_invalid_passed = False
        except:
            print(f"   ❌ Invalid login test FAILED (no error message element) for {test_user}/{test_pass}")
            all_invalid_passed = False

        # Return to login page before next invalid combo
        driver.get("http://127.0.0.1:5000/")
        time.sleep(1)

    if all_invalid_passed:
        print("✅ All invalid login attempts displayed error messages as expected.")
    else:
        print("❌ One or more invalid login attempts did not show the expected error.")

    # ----------------------------------------------------------------------------
    # Test Case 2: Valid Login with Email
    # ----------------------------------------------------------------------------
    print("\n🔹 Test Case 2: Valid Login with Email")
    driver.get("http://127.0.0.1:5000/")
    time.sleep(1)

    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("user@example.com")

    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("password123")

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(2)

    # Check if login was successful
    if "Login Successful" in driver.page_source:
        print("✅ Valid email login test PASSED.")
    else:
        print("❌ Valid email login test FAILED.")

    # NOTE: We intentionally do NOT log out here so we can do further checks below.

    # ----------------------------------------------------------------------------
    # Test Case 3: Valid Login with Phone Number (Overriding previous session)
    # ----------------------------------------------------------------------------
    print("\n🔹 Test Case 3: Valid Login with Phone Number")
    # Even if still logged in, we'll revisit the login page and try new credentials
    driver.get("http://127.0.0.1:5000/")
    time.sleep(1)

    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("1234567890")  # phone user

    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("mypassword")

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(2)

    # Check if login was successful
    if "Login Successful" in driver.page_source:
        print("✅ Valid phone login test PASSED.")
    else:
        print("❌ Valid phone login test FAILED.")

    # ----------------------------------------------------------------------------
    # Test Case 4: Logout After Successful Login
    # ----------------------------------------------------------------------------
    print("\n🔹 Test Case 4: Logout After Successful Login")

    # We should still be logged in from Test Case 3. Let's confirm or just proceed:
    driver.get("http://127.0.0.1:5000/success")
    time.sleep(1)
    if "Login Successful" not in driver.page_source:
        print("   ❗ We are not on the success page; attempting to log in again.")
        # If for some reason not logged in, log in again quickly
        driver.get("http://127.0.0.1:5000/")
        time.sleep(1)
        username_input = driver.find_element(By.NAME, "username")
        username_input.clear()
        username_input.send_keys("1234567890")  # phone user
        password_input = driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys("mypassword")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        time.sleep(2)

    # Now do logout
    driver.get("http://127.0.0.1:5000/logout")
    time.sleep(2)

    # After logout, we expect to be redirected to the login page
    if "Login Page" in driver.page_source or "Login" in driver.title:
        print("✅ Logout test PASSED (redirected to login page).")
    else:
        print("❌ Logout test FAILED (not redirected to login page).")

    # ----------------------------------------------------------------------------
    # Test Case 5: Google OAuth Login Button
    # ----------------------------------------------------------------------------
    print("\n🔹 Test Case 5: Google OAuth Login Button")
    driver.get("http://127.0.0.1:5000/")
    time.sleep(1)

    google_login_button = driver.find_element(By.XPATH, "//a[contains(@href, 'login/google')]")
    google_login_button.click()
    time.sleep(3)

    # Verify redirection to Google (Check if the URL contains "accounts.google.com")
    current_url = driver.current_url
    if "accounts.google.com" in current_url:
        print("✅ Google login button test PASSED (redirected to Google).")
    else:
        print(f"❌ Google login button test FAILED (no redirection). Current URL: {current_url}")

except Exception as e:
    print(f"\n❌ Test failed due to unexpected error: {e}")

finally:
    # ✅ Close the browser
    time.sleep(2)
    driver.quit()
