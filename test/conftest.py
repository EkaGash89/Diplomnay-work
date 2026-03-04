"""
Конфигурационный файл для pytest с фикстурами
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def pytest_configure(config):
    """Конфигурация pytest при запуске."""
    config.addinivalue_line("markers", "positive: Позитивные тесты")
    config.addinivalue_line("markers", "negative: Негативные тесты")
    config.addinivalue_line("markers", "ui: UI тесты")
    config.addinivalue_line("markers", "smoke: Smoke тесты")
    config.addinivalue_line("markers", "regression: Регрессионные тесты")


@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для создания и закрытия WebDriver.
    """
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()