# selenium_tests/test_tree_flow.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("login_contributor")
def test_full_tree_flow(login_contributor):
    driver = login_contributor

    # --- Navigate to Map page via navbar ---
    map_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Map"))
    )
    map_link.click()

    # Wait until map page loads
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "map")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tree-form")))

    # --- Fill in Add Tree form ---
    driver.find_element(By.NAME, "street_name").send_keys("Test Tree")
    driver.find_element(By.NAME, "scientific_name").send_keys("Ficus testicus")
    driver.find_element(By.NAME, "habitat").send_keys("Urban Park")
    driver.find_element(By.NAME, "description").send_keys("A test tree.")
    driver.find_element(By.NAME, "rarity_status").send_keys("Rare")
    driver.find_element(By.NAME, "height_m").send_keys("5.5")
    driver.find_element(By.NAME, "age_estimate").send_keys("12")

    # --- Set lat/lng manually ---
    driver.execute_script("""
        document.getElementById('id_latitude').value = '23.8103';
        document.getElementById('id_longitude').value = '90.4125';
    """)

    # --- Submit form ---
    driver.find_element(By.CSS_SELECTOR, "#tree-form button[type='submit']").click()

    # --- Wait for JS alert confirming tree addition ---
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert "Tree added successfully" in alert.text
    alert.accept()

    # --- Verify marker exists on map (Leaflet markers have 'leaflet-marker-icon' class) ---
    marker = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-marker-icon"))
    )
    assert marker is not None
    
    print("✅ Full tree flow test passed!")
