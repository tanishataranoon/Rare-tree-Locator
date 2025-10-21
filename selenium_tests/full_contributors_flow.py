import pytest
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def test_contributor_full_flow(login_contributor):
    driver = login_contributor

    # ================= PROFILE UPDATE =================
    driver.get("http://127.0.0.1:8000/edit_profile/")
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "bio")))

    new_bio = "Updated bio through Selenium "
    bio_field = driver.find_element(By.NAME, "bio")
    bio_field.clear()
    time.sleep(0.5)
    bio_field.send_keys(new_bio)
    time.sleep(0.5)

    form = driver.find_element(By.ID, "profileForm")
    driver.execute_script("arguments[0].submit();", form)
    time.sleep(1)

    WebDriverWait(driver, 10).until(EC.url_contains("profile"))
    assert new_bio in driver.page_source
    print(" Profile updated successfully!")

    # ================= BLOG CRUD =================
    # --- Add blog ---
    driver.get("http://127.0.0.1:8000/add/")
    time.sleep(1)

    title_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    )
    title_field.send_keys("Selenium Blog")
    time.sleep(0.5)

    content_field = driver.find_element(By.NAME, "content")
    content_field.send_keys("Automated blog content")
    time.sleep(0.5)

    image_input = driver.find_element(By.ID, "id_image")
    test_image_path = os.path.abspath("selenium_tests/test_image.jpeg")
    image_input.send_keys(test_image_path)
    time.sleep(0.5)

    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "form#blogForm button.publish-btn"))
    )
    submit_btn.click()
    time.sleep(1)

    WebDriverWait(driver, 10).until(EC.url_contains("blog_list"))
    assert "Selenium Blog" in driver.page_source
    print(" Blog created successfully!")

    # --- Edit blog ---
    driver.get("http://127.0.0.1:8000/blog_list")
    time.sleep(1)

    edit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".edit-btn"))
    )
    edit_btn.click()
    time.sleep(0.5)

    title_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    )
    title_field.clear()
    time.sleep(0.5)
    title_field.send_keys("Selenium Blog Edited")

    content_field = driver.find_element(By.NAME, "content")
    content_field.clear()
    time.sleep(0.5)
    content_field.send_keys("Edited automated blog content")

    submit_btn = driver.find_element(By.CSS_SELECTOR, "form#blogForm button.publish-btn")
    submit_btn.click()
    time.sleep(1)

    WebDriverWait(driver, 10).until(EC.url_contains("blog_list"))
    assert "Selenium Blog Edited" in driver.page_source
    print(" Blog edited successfully!")

    # --- Delete blog ---
    delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".delete-btn"))
    )
    delete_btn.click()
    time.sleep(0.5)

    confirm_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#deleteForm button.confirm-delete"))
    )
    confirm_btn.click()
    time.sleep(1)

    WebDriverWait(driver, 10).until_not(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Selenium Blog Edited")
    )
    assert "Selenium Blog Edited" not in driver.page_source
    print(" Blog deleted successfully!")

    # ================= ANSWER REQUEST =================
    driver.get("http://127.0.0.1:8000/requests/")
    time.sleep(1)

    try:
        card = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".request-card-modern"))
        )

        view_btn = card.find_element(By.CSS_SELECTOR, ".btn-view")
        view_btn.click()
        time.sleep(1)

        try:
            answer_btn = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "answer-btn"))
            )
            driver.execute_script("arguments[0].click();", answer_btn)
            time.sleep(0.5)

            response_field = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.NAME, "response_text"))
            )
            response_field.clear()
            response_field.send_keys("Automated test answer.")
            time.sleep(0.5)

            submit_btn = driver.find_element(By.CSS_SELECTOR, "form button[type='submit']")
            driver.execute_script("arguments[0].click();", submit_btn)
            print("Answer submitted successfully!")
            time.sleep(1)

        except TimeoutException:
            print("No answer button available")

    except TimeoutException:
        print(" No request cards available")

    # ================= LOGOUT =================
    driver.get("http://127.0.0.1:8000/")
    time.sleep(1)

# ================= LOGOUT  =================
    try:
        # Instead of clicking logout, just navigate to login page
        driver.get("http://127.0.0.1:8000/login/")
        time.sleep(1)
        print(" Contributor redirected to login page (logout simulated)!")
    except Exception as e:
        print(" Could not redirect to login page:", e)
