import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.order(2)
def test_blog_flow(login_contributor):
    driver = login_contributor

    # ------------------- ADD BLOG -------------------
    driver.get("http://127.0.0.1:8000/add/")

    # Fill title and content
    title_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    )
    title_field.send_keys("Selenium Blog")

    content_field = driver.find_element(By.NAME, "content")
    content_field.send_keys("Automated blog content")

    # Upload an image
    image_input = driver.find_element(By.ID, "id_image")
    # Use a small test image in your project folder, e.g., tests/test_image.png
    test_image_path = os.path.abspath("selenium_tests/test_image.jpeg")
    image_input.send_keys(test_image_path)

    # Click submit
    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "form#blogForm button.publish-btn"))
    )
    submit_btn.click()

    # Verify redirect to blog list
    WebDriverWait(driver, 10).until(EC.url_contains("blog_list"))
    assert "Selenium Blog" in driver.page_source
    print("✅ Blog created successfully!")

    # ------------------- EDIT BLOG -------------------
    driver.get("http://127.0.0.1:8000/blog_list")
    edit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".edit-btn"))
    )
    edit_btn.click()

    # Change title and content
    title_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    )
    title_field.clear()
    title_field.send_keys("Selenium Blog Edited")

    content_field = driver.find_element(By.NAME, "content")
    content_field.clear()
    content_field.send_keys("Edited automated blog content")

    submit_btn = driver.find_element(By.CSS_SELECTOR, "form#blogForm button.publish-btn")
    submit_btn.click()

    WebDriverWait(driver, 10).until(EC.url_contains("blog_list"))
    assert "Selenium Blog Edited" in driver.page_source
    print("✅ Blog edited successfully!")

    # ------------------- DELETE BLOG -------------------
    delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".delete-btn"))
    )
    delete_btn.click()

    # Confirm delete in modal
    confirm_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#deleteForm button.confirm-delete"))
    )
    confirm_btn.click()

    WebDriverWait(driver, 10).until(EC.url_contains("blog_list"))
    assert "Selenium Blog Edited" not in driver.page_source
    print("✅ Blog deleted successfully!")
