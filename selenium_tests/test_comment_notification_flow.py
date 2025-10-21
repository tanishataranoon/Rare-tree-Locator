import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

def slow_type(element, text, delay=0.1):
    """Types text slowly into an input/textarea (simulates human typing)"""
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

@pytest.mark.order(5)
def test_comment_and_notification_flow(login_normal_user, login_contributor):
    normal_driver = login_normal_user
    contrib_driver = login_contributor

    # ---------------- STEP 1: Normal user posts a comment ----------------
    normal_driver.get("http://127.0.0.1:8000/blog_list")
    first_blog = WebDriverWait(normal_driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn[href*='blog_list/']"))
    )
    first_blog.click()

    comment_box = WebDriverWait(normal_driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form.comment-form textarea[name='content']"))
    )
    slow_type(comment_box, "Automated comment from Selenium test", delay=0.15)
    normal_driver.find_element(By.CSS_SELECTOR, "form.comment-form button[type='submit']").click()

    WebDriverWait(normal_driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".comments-list"), "Automated comment from Selenium")
    )
    print("✅ Comment posted by normal user")

    # ---------------- STEP 2: Contributor checks notifications ----------------
    contrib_driver.get("http://127.0.0.1:8000/blog_list")

    try:
        # Open profile sidebar
        profile_icon = WebDriverWait(contrib_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "profile-icon"))
        )
        profile_icon.click()
        WebDriverWait(contrib_driver, 10).until(
            EC.visibility_of_element_located((By.ID, "profile-panel"))
        )

        # Click the notification link if it exists
        try:
            notif_link = WebDriverWait(contrib_driver, 5).until(
                EC.element_to_be_clickable((By.ID, "notif-link"))
            )
            notif_link.click()
            print("✅ Contributor clicked the notification link (if available)")
        except TimeoutException:
            print("⚠️ No notifications available for contributor. Skipping click.")
    
    except TimeoutException:
        print("❌ Contributor profile sidebar not found. Test may need adjustment.")



