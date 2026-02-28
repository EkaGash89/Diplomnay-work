from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure

class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator, timeout=10):
        """Поиск элемента с ожиданием"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="element_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            raise NoSuchElementException(f"Элемент {locator} не найден за {timeout} секунд")
    
    def find_clickable_element(self, locator, timeout=10):
        """Поиск кликабельного элемента"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="element_not_clickable",
                attachment_type=allure.attachment_type.PNG
            )
            raise NoSuchElementException(f"Элемент {locator} не кликабелен за {timeout} секунд")
    
    def send_keys(self, locator, text, clear_first=True):
        """Ввод текста в поле"""
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def click(self, locator):
        """Клик по элементу"""
        element = self.find_clickable_element(locator)
        element.click()
    
    def get_text(self, locator):
        """Получение текста элемента"""
        element = self.find_element(locator)
        return element.text
    
    def get_attribute(self, locator, attribute):
        """Получение атрибута элемента"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)
    
    def is_element_present(self, locator, timeout=5):
        """Проверка наличия элемента на странице"""
        try:
            self.find_element(locator, timeout)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_url_contains(self, text, timeout=10):
        """Ожидание, что URL содержит текст"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.url_contains(text))
            return True
        except TimeoutException:
            return False
    
    def take_screenshot(self, name="screenshot"):
        """Создание скриншота"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
            )