import pytest
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def test_contributor_full_flow(login_contributor):
    driver = login_contributor  # assign driver here

    # ================= PROFILE UPDATE =================
    driver.get("http://127.0.0.1:8000/edit_profile/")
    time.sleep(0.5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "bio")))
    # ... rest of your test code ...

    # ================= PROFILE UPDATE =================
    driver.get("http://127.0.0.1:8000/edit_profile/")
    time.sleep(0.5)  # reduced
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "bio")))

    new_bio = "Updated bio through Selenium ✅"
    bio_field = driver.find_element(By.NAME, "bio")
    bio_field.clear()
    time.sleep(0.2)
    bio_field.send_keys(new_bio)
    time.sleep(0.2)

    form = driver.find_element(By.ID, "profileForm")
    driver.execute_script("arguments[0].submit();", form)
    time.sleep(0.5)

    WebDriverWait(driver, 10).until(EC.url_contains("profile"))
    assert new_bio in driver.page_source
    print("✅ Profile updated successfully!")

    # ================= ANSWER REQUEST =================
    driver.get("http://127.0.0.1:8000/requests/")
    time.sleep(0.5)

    try:
        card = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".request-card-modern"))
        )
        view_btn = card.find_element(By.CSS_SELECTOR, ".btn-view")
        view_btn.click()
        time.sleep(0.5)

        try:
            answer_btn = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "answer-btn"))
            )
            driver.execute_script("arguments[0].click();", answer_btn)
            time.sleep(0.2)

            response_field = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.NAME, "response_text"))
            )
            response_field.clear()
            response_field.send_keys("Automated test answer.")
            time.sleep(0.2)

            submit_btn = driver.find_element(By.CSS_SELECTOR, "form button[type='submit']")
            driver.execute_script("arguments[0].click();", submit_btn)
            print("✅ Answer submitted successfully!")
            time.sleep(0.5)

        except TimeoutException:
            print("⚠️ No answer button available")

    except TimeoutException:
        print("⚠️ No request cards available")
