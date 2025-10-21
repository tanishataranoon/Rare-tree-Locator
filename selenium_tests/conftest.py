import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Shared WebDriver for the session ---
@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


# --- Contributor login fixture ---
@pytest.fixture(scope="session")
def login_contributor(driver):
    driver.get("http://127.0.0.1:8000/login/")

    # Login fields
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    # Fill credentials (your contributor account)
    username_field.send_keys("hridy")  
    password_field.send_keys("gN8zyQ2NWX-5GKn", Keys.RETURN)

    # Wait until redirected to profile page
    WebDriverWait(driver, 10).until(EC.url_contains("profile"))
    print("✅ Successfully logged in as contributor. Redirected to profile page.")

    # Return driver so other tests can continue
    return driver


# --- Normal user login fixture ---
@pytest.fixture(scope="session")
def login_normal_user(driver):
    driver.get("http://127.0.0.1:8000/login/")

    # Login fields
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    # Fill credentials (normal user account)
    username_field.send_keys("tan")  
    password_field.send_keys("<3yourself97", Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.url_contains("profile"))
    print("✅ Successfully logged in as Common  user. Redirected to profile page.")

    return driver
