import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.run(order=4)  
@pytest.mark.usefixtures("login_contributor")
def test_tree_search_flow(login_contributor):
    driver = login_contributor

    # --- Step 1: Go to "Trees" page ---
    trees_link = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Trees"))
    )
    trees_link.click()

    # --- Step 2: Wait for search box ---
    search_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "treeSearch"))
    )
    search_box.clear()
    search_box.send_keys("Test Tree")

    # --- Step 3: Click the search button ---
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "searchBtn"))
    )
    search_button.click()

    # --- Step 4: Wait for search results (cards) ---
    cards = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
    )

    assert len(cards) > 0, "No tree cards found after search!"

    # --- Step 5: Click 'View Details' inside first card ---
    first_card = cards[0]

    view_button = WebDriverWait(first_card, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.view-details-btn"))
    )
    view_button.click()

    # --- Step 6: Wait for detail page to load ---
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )

    current_url = driver.current_url
    assert "/tree/" in current_url or "detail" in current_url, "Did not navigate to tree detail page!"

    print("✅ Tree search and detail open flow successful!")
