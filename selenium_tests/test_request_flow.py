import os
import sys
import django
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

# Step 1: Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Step 2: Set Django settings and initialize
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rare_Tree_locator.settings")
django.setup()


@pytest.mark.order(4)
def test_tree_request_creation_then_profile(login_normal_user):
    driver = login_normal_user
    username = "tan"

    # Go to Tree Requests page
    driver.get("http://127.0.0.1:8000/tree-requests/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "new-request-btn")))

    # Click New Request and fill form
    driver.find_element(By.ID, "new-request-btn").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "new-request-form")))

    driver.find_element(By.NAME, "title").send_keys("Test Tree Request")
    driver.find_element(By.NAME, "description").send_keys("This is a test description")
    driver.find_element(By.NAME, "location").send_keys("Test Location")
    driver.find_element(By.CSS_SELECTOR, "#new-request-form button[type='submit']").click()

    # Optional: wait for alert
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = Alert(driver)
        print("ALERT:", alert.text)
        alert.accept()
    except Exception:
        print("⚠️ No alert appeared after submission — continuing test...")

    # Go back to profile page to check if the request appears there
    driver.get(f"http://127.0.0.1:8000/profile_view/{username}/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))

    # Check that the new request is mentioned on the profile page
    assert "Test Tree Request" in driver.page_source
    print("✅ Request creation verified on profile page.")
