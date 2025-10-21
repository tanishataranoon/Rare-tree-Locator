# import os
# import sys
# import django

# # ---------------- Django setup ----------------
# # Add the project root (same level as manage.py) to Python path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # Set Django settings module (use underscore if your folder is 'Rare_tree_Locator')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rare_tree_Locator.settings')

# # Initialize Django
# django.setup()

# # ---------------- Imports after setup ----------------
# import pytest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from DonationApp.models import Donation
# from django.contrib.auth import get_user_model
# import time


# @pytest.mark.order(6)
# @pytest.mark.django_db
# def test_donation_flow_dashboard(login_normal_user, db):
#     driver = login_normal_user

#     # ---------------- STEP 1: Go to homepage and fill donation ----------------
#     driver.get("http://127.0.0.1:8000/")

#     amount_input = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.NAME, "amount"))
#     )
#     amount_input.clear()
#     amount_input.send_keys("100")

#     donate_btn = driver.find_element(By.CSS_SELECTOR, "button.donation-btn")
#     donate_btn.click()

#     # ---------------- STEP 2: Wait for SSLCommerz sandbox redirect ----------------
#     WebDriverWait(driver, 10).until(lambda d: "sandbox.sslcommerz.com" in d.current_url)
#     print("✅ Redirected to SSLCommerz sandbox page")

#     # ---------------- STEP 3: Verify donation record in DB ----------------
#     User = get_user_model()
#     user = User.objects.get(username="tan")

#     donation = Donation.objects.filter(user=user, amount=100).last()
#     assert donation is not None, "Donation record not created"
#     assert donation.status == "PENDING", f"Expected PENDING, got {donation.status}"
#     print(f"✅ Donation record created with order_id: {donation.order_id}")

#     # ---------------- STEP 4: Simulate successful payment ----------------
#     donation.status = "PAID"
#     donation.save()
#     print("✅ Donation status manually set to PAID for testing dashboard history")

#     # ---------------- STEP 5: Verify donation appears in dashboard ----------------
#     driver.get("http://127.0.0.1:8000/dashboard/donation-history/")

#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located(
#             (By.XPATH, f"//td[contains(text(), '{donation.order_id}')]")
#         )
#     )
#     print("✅ Donation appears in dashboard history with PAID status")
