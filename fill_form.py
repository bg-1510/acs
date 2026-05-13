import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# ─── Configuration ────────────────────────────────────────────────────────────
DHR_URL = "https://contactbhromor.github.io/acs/"

# Values are read from environment variables (set as GitHub Secrets)
# Falls back to "0" if a secret is not set
INPUT_VALUES = [
    os.getenv("DHR_Q1",  "0"),   # Business impacting outages
    os.getenv("DHR_Q2",  "0"),   # P0/P1 tickets breached SLA
    os.getenv("DHR_Q3",  "0"),   # P2/Sev2 tickets breached SLA
    os.getenv("DHR_Q4",  "0"),   # Ticket backlog %
    os.getenv("DHR_Q5",  "0"),   # Critical MTD breached SLAs
    os.getenv("DHR_Q6",  "0"),   # Process deviations / human errors
    os.getenv("DHR_Q7",  "0"),   # Operational escalations
    os.getenv("DHR_Q8",  "0"),   # Changes deployed
    os.getenv("DHR_Q9",  "0"),   # Change failures
    os.getenv("DHR_Q10", "0"),   # Security incidents / vulnerabilities
    os.getenv("DHR_Q11", "0"),   # Compliance violations
    os.getenv("DHR_Q12", "0"),   # Audit findings
    os.getenv("DHR_Q13", "0"),   # Attrition %
    os.getenv("DHR_Q14", "0"),   # Unplanned absenteeism
    os.getenv("DHR_Q15", "0"),   # Escalations from internal stakeholders
]
# ──────────────────────────────────────────────────────────────────────────────


def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=options)


def fill_form():
    driver = get_driver()
    wait = WebDriverWait(driver, 15)

    try:
        print(f"Opening {DHR_URL}")
        driver.get(DHR_URL)
        time.sleep(2)

        # Step 1: Select MICROSOFT
        dropdown = wait.until(EC.presence_of_element_located((By.ID, "parentCustomer")))
        Select(dropdown).select_by_value("MICROSOFT")
        print("Selected MICROSOFT from dropdown")
        time.sleep(1)

        # Step 2: Fill each input
        for idx, value in enumerate(INPUT_VALUES):
            try:
                field = wait.until(EC.visibility_of_element_located((By.ID, f"input_{idx}")))
                field.clear()
                field.send_keys(value)
                print(f"  Q{idx + 1}: set to {value!r}")
            except Exception as e:
                print(f"  Q{idx + 1}: could not fill — {e}")

        # Step 3: Submit
        submit_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn-submit')]"))
        )
        submit_btn.click()
        print("Clicked Submit — form submitted successfully.")
        time.sleep(2)

    except Exception as ex:
        print(f"ERROR: {ex}")
        driver.save_screenshot("error_screenshot.png")
        raise

    finally:
        driver.quit()


if __name__ == "__main__":
    print("── DHR values loaded from environment ──")
    for i, v in enumerate(INPUT_VALUES):
        print(f"  Q{i+1}: {v}")
    print("────────────────────────────────────────")
    fill_form()
