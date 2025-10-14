from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# start Chrome (webdriver-manager finds/installs the proper chromedriver)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://www.google.com")
    # explicit wait for the search box
    wait = WebDriverWait(driver, 10)
    box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    box.send_keys("Selenium python")
    box.submit()
    # wait for results
    wait.until(EC.presence_of_element_located((By.ID, "search")))
    print("Search results loaded — test passed")
finally:
    driver.quit()
