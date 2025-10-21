import os
import sys
import django
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException

# ----------------- Django setup -----------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rare_Tree_locator.settings")
django.setup()

# ----------------- Helper -----------------
def slow_type(element, text, delay=0.05):
    """Types text slowly into an input/textarea (simulates human typing)"""
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

# ----------------- Fixture -----------------
@pytest.fixture(scope="session")
def login_normal_user(driver):
    driver.get("http://127.0.0.1:8000/login/")
    driver.find_element(By.NAME, "username").send_keys("tan")
    driver.find_element(By.NAME, "password").send_keys("<3yourself97", Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.url_contains("profile"))
    print("✅ Successfully logged in as common user.")
    return driver

# ----------------- Test: Common User Full Flow -----------------
@pytest.mark.order(1)
def test_common_user_full_flow(login_normal_user):
    driver = login_normal_user
    username = "tan"

    # ================= PROFILE UPDATE =================
    driver.get("http://127.0.0.1:8000/edit_profile/")
    bio_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "bio"))
    )

    new_bio = "Updated bio via Selenium (common user)"
    bio_field.clear()
    slow_type(bio_field, new_bio)

    form = driver.find_element(By.ID, "profileForm")
    driver.execute_script("arguments[0].submit();", form)
    WebDriverWait(driver, 10).until(EC.url_contains("profile"))

    # Verify profile update (search text anywhere on page)
    driver.get(f"http://127.0.0.1:8000/profile_view/{username}/")
    bio_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(text(), '{new_bio}')]")
        )
    )
    assert new_bio in bio_element.text
    print("✅ Profile updated successfully!")

    # ================= CREATE TREE REQUEST =================
    driver.get("http://127.0.0.1:8000/tree-requests/")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "new-request-btn"))
    ).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "new-request-form")))

    driver.find_element(By.NAME, "title").send_keys("Common User Test Tree Request")
    driver.find_element(By.NAME, "description").send_keys("This is a test description")
    driver.find_element(By.NAME, "location").send_keys("Test Location")
    driver.find_element(By.CSS_SELECTOR, "#new-request-form button[type='submit']").click()

    # Handle optional alert
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = Alert(driver)
        print("ALERT:", alert.text)
        alert.accept()
    except TimeoutException:
        print("⚠️ No alert appeared after submission.")

    # ================= POST COMMENT ON BLOG =================
    driver.get("http://127.0.0.1:8000/blog_list")
    first_blog = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn[href*='blog_list/']"))
    )
    first_blog.click()

    comment_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form.comment-form textarea[name='content']"))
    )
    slow_type(comment_box, "Automated comment from Selenium test")
    driver.find_element(By.CSS_SELECTOR, "form.comment-form button[type='submit']").click()

    # Verify comment appears in comment list
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, ".comments-list"), "Automated comment from Selenium"
        )
    )
    print("✅ Comment posted successfully!")
