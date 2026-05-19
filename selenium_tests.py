from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = "http://localhost"

def get_driver():
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def test_homepage_loads():
    """Test 1: Verify homepage loads successfully"""
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        time.sleep(2)
        assert "Wajdan Agency" in driver.title or "Wajdan" in driver.page_source
        print("✅ Test 1 PASSED: Homepage loads successfully")
    except Exception as e:
        print(f"❌ Test 1 FAILED: {e}")
    finally:
        driver.quit()

def test_dashboard_stats_visible():
    """Test 2: Verify dashboard stats are visible"""
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        time.sleep(2)
        page = driver.page_source
        assert "Total Clients" in page
        assert "Total Invoices" in page
        print("✅ Test 2 PASSED: Dashboard stats are visible")
    except Exception as e:
        print(f"❌ Test 2 FAILED: {e}")
    finally:
        driver.quit()

def test_navigation_clients():
    """Test 3: Verify Clients navigation works"""
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        time.sleep(2)
        clients_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Clients')]")
        clients_btn.click()
        time.sleep(2)
        assert "Add New Client" in driver.page_source
        print("✅ Test 3 PASSED: Clients navigation works")
    except Exception as e:
        print(f"❌ Test 3 FAILED: {e}")
    finally:
        driver.quit()

def test_navigation_invoices():
    """Test 4: Verify Invoices navigation works"""
    driver = get_driver()
    try:
        driver.get(BASE_URL)
        time.sleep(2)
        invoice_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Invoices')]")
        invoice_btn.click()
        time.sleep(2)
        assert "Create Invoice" in driver.page_source
        print("✅ Test 4 PASSED: Invoices navigation works")
    except Exception as e:
        print(f"❌ Test 4 FAILED: {e}")
    finally:
        driver.quit()

def test_backend_api_health():
    """Test 5: Verify backend API is reachable"""
    import urllib.request
    try:
        response = urllib.request.urlopen("http://localhost:5000/health")
        data = response.read().decode()
        assert "ok" in data
        print("✅ Test 5 PASSED: Backend API is healthy")
    except Exception as e:
        print(f"❌ Test 5 FAILED: {e}")

if __name__ == "__main__":
    print("🚀 Running Selenium Tests for Wajdan Agency CMS")
    print("=" * 50)
    test_homepage_loads()
    test_dashboard_stats_visible()
    test_navigation_clients()
    test_navigation_invoices()
    test_backend_api_health()
    print("=" * 50)
    print("✅ All tests completed!")