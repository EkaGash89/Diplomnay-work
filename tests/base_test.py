import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException

class BaseTest:
    """Базовый класс для всех тестов с общими методами"""
    
    def setup_method(self):
        """Настройка перед тестом"""
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "https://www.chitai-gorod.ru"
        
        print("\n" + "="*70)
        print("🚀 ЗАПУСК ТЕСТИРОВАНИЯ")
        print("="*70)
    
    def teardown_method(self):
        """Очистка после теста"""
        if self.driver:
            self.driver.quit()
    
    def find_element_by_selectors(self, selectors, element_description="элемент"):
        """Поиск элемента по списку селекторов"""
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        print(f"✅ Нашли {element_description} по селектору: {selector}")
                        return element
            except:
                continue
        print(f"⚠️ {element_description} не найден")
        return None
    
    def find_elements_by_selectors(self, selectors, element_description="элементы"):
        """Поиск всех элементов по списку селекторов"""
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Нашли {element_description} по селектору: {selector} (найдено: {len(elements)})")
                    return elements
            except:
                continue
        return []
    
    def click_element(self, element, description="элемент"):
        """Безопасный клик по элементу"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            element.click()
            return True
        except Exception as e:
            print(f"⚠️ Ошибка при клике на {description}: {e}")
            return False
    
    def scroll_to_element(self, element):
        """Прокрутка до элемента"""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)
    
    def close_banner(self):
        """Закрытие баннера"""
        close_selectors = [
            "button[aria-label='Закрыть']",
            ".banner-close",
            ".modal-close",
            ".popup-close",
            "button.close",
            "img[alt='close']",
            ".chg-popup__close",
            "[class*='close']"
        ]
        
        for selector in close_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        print("🔍 Нашли кнопку закрытия баннера")
                        element.click()
                        time.sleep(1)
                        print("✅ Баннер закрыт")
                        return True
            except:
                continue
        
        print("ℹ️ Баннер не найден или уже закрыт")
        return False
    
    def force_set_value(self, field, value):
        """Принудительная установка значения через JavaScript"""
        try:
            self.driver.execute_script(f"arguments[0].value = '{value}';", field)
            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, field)
            time.sleep(0.5)
            return field.get_attribute('value') == value
        except Exception as e:
            print(f"⚠️ Ошибка при установке значения: {e}")
            return False
    
    def clear_field_reliably(self, field):
        """Надежная очистка поля"""
        try:
            field.clear()
            time.sleep(0.5)
            
            if field.get_attribute('value') == "":
                return True
            
            self.driver.execute_script("arguments[0].value = '';", field)
            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, field)
            
            return field.get_attribute('value') == ""
        except Exception as e:
            print(f"⚠️ Ошибка при очистке поля: {e}")
            return False
    
    def check_field_visible_and_enabled(self, field):
        """Проверка, что поле видимо и доступно"""
        try:
            if not field.is_displayed():
                print("⚠️ Поле не отображается на странице")
                self.scroll_to_element(field)
            
            if not field.is_enabled():
                print("⚠️ Поле отключено")
                return False
            
            return True
        except Exception as e:
            print(f"⚠️ Ошибка при проверке поля: {e}")
            return False
    
    def check_error_message(self):
        """Проверка наличия сообщения об ошибке на странице"""
        error_selectors = [
            ".chg-input__error",
            ".error-message",
            ".chg-notification__error",
            ".chg-input--error",
            "[class*='error']"
        ]
        
        for selector in error_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        print(f"⚠️ Найдено сообщение об ошибке: {element.text}")
                        return True
            except:
                continue
        return False
    
    def print_separator(self, title="", char="=", length=70):
        """Вывод разделителя с заголовком"""
        print("\n" + char * length)
        if title:
            print(f"{title:^{length}}")
            print(char * length)