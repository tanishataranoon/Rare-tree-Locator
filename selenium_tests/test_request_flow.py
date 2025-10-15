import pytest
import os
import sys
import django
# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FinalProject.settings")

# Setup Django
django.setup()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from TreeApp.models import TreeRequest


@pytest.mark.django_db
def test_tree_request_flow(login_normal_user):
    driver = login_normal_user
    username = "teacher"  # your normal user

    # 1️⃣ Land on profile page
    driver.get(f"http://127.0.0.1:8000/profile_view/{username}/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h2"))
    )
    assert username in driver.page_source

    # 2️⃣ Go to dashboard
    driver.get("http://127.0.0.1:8000/dashboard/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "main.dashboard-content"))
    )
    assert "Dashboard" in driver.page_source

    # 3️⃣ Go to Tree Requests page
    driver.get("http://127.0.0.1:8000/tree-requests/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "new-request-btn"))
    )

    # 4️⃣ Open modal to create new request
    driver.find_element(By.ID, "new-request-btn").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "new-request-form"))
    )

    # Fill the form
    driver.find_element(By.NAME, "title").send_keys("Test Tree Request")
    driver.find_element(By.NAME, "description").send_keys("This is a test description")
    driver.find_element(By.NAME, "location").send_keys("Test Location")

    # Submit form
    driver.find_element(By.CSS_SELECTOR, "#new-request-form button[type='submit']").click()

    # 5️⃣ Handle alert immediately
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert_text = alert.text
    assert "Request created successfully!" in alert_text
    alert.accept()

    # 6️⃣ Wait until the request appears in the table
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
        (By.XPATH, "//td[contains(text(),'Test Tree Request')]")
        )
    )

    assert "Test Tree Request" in driver.page_source

    # 7️⃣ Delete the request
    delete_button = driver.find_element(
        By.XPATH,
        "//td[contains(text(),'Test Tree Request')]/following-sibling::td/button[contains(@class,'delete-request')]"
    )
    delete_button.click()

    # Wait until the row disappears
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located(
            (By.XPATH, "//td[contains(text(),'Test Tree Request')]")
        )
    )
    assert "Test Tree Request" not in driver.page_source
# After accepting alert
    alert.accept()

# Reload the page so the table contains the new request
    driver.refresh()

# Now wait for the row
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
        (By.XPATH, "//td[contains(text(),'Test Tree Request')]")
        )
)
