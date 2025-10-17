import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.mark.run(order=1)  # runs first
def test_login_profile(login_contributor):
    driver = login_contributor
    driver.get("http://127.0.0.1:8000/edit_profile/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "bio")))

    new_bio = "Updated bio through Selenium ✅"
    bio_field = driver.find_element(By.NAME, "bio")
    bio_field.clear()
    bio_field.send_keys(new_bio)

    form = driver.find_element(By.ID, "profileForm")
    driver.execute_script("arguments[0].submit();", form)
    WebDriverWait(driver, 10).until(EC.url_contains("profile"))
    assert new_bio in driver.page_source
    