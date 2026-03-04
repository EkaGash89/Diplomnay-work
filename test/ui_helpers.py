"""
Вспомогательные функции для UI тестов
"""

import time
import re
from typing import Optional, Tuple, List, Any, Dict
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import allure


# ========== Базовые функции работы с элементами ==========

def wait_and_find_element(driver, locator: Tuple, timeout: int = 10) -> Optional[WebElement]:
    """Ожидание появления элемента и его возврат."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element
    except TimeoutException:
        return None


def wait_and_click(driver, locator: Tuple, timeout: int = 10) -> bool:
    """Ожидание кликабельности элемента и клик по нему."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return True
    except TimeoutException:
        return False


def clear_and_send_keys(driver, locator: Tuple, text: str, timeout: int = 10) -> bool:
    """Очистка поля и ввод текста."""
    element = wait_and_find_element(driver, locator, timeout)
    if element:
        element.clear()
        element.send_keys(text)
        return True
    return False


def safe_click(driver, element: WebElement, use_js_fallback: bool = True) -> bool:
    """Безопасный клик с возможностью JavaScript fallback."""
    try:
        element.click()
        return True
    except Exception as e:
        if use_js_fallback:
            try:
                driver.execute_script("arguments[0].click();", element)
                return True
            except:
                pass
        print(f"  Ошибка клика: {e}")
        return False


def scroll_to_element(driver, element: WebElement, block: str = 'center') -> None:
    """Скролл до элемента."""
    driver.execute_script(f"arguments[0].scrollIntoView({{block: '{block}'}});", element)
    time.sleep(0.5)


# ========== Функции для работы с баннерами/попапами ==========

class BannerHandler:
    """Класс для обработки баннеров и попапов."""
    
    @staticmethod
    def kill_all_banners(driver) -> bool:
        """Уничтожение всех баннеров и попапов на странице."""
        try:
            popups = driver.find_elements(By.CLASS_NAME, "popmechanic-main")
            if popups:
                print(f"  Обнаружено баннеров: {len(popups)}")
                
                close_selectors = [
                    ".popmechanic-close",
                    ".popup__close",
                    ".modal__close",
                    "button.close",
                    "[aria-label='Закрыть']",
                ]
                
                for selector in close_selectors:
                    buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in buttons:
                        try:
                            if btn.is_displayed():
                                btn.click()
                                print(f"  Баннер закрыт через {selector}")
                                time.sleep(1)
                                return True
                        except:
                            pass
                
                # Если не нашли кнопку, пробуем ESC
                body = driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ESCAPE)
                print("  Баннер закрыт через ESC")
                time.sleep(1)
                return True
        except Exception as e:
            print(f"  Ошибка при закрытии баннеров: {e}")
        return False
    
    @staticmethod
    def close_popup_if_exists(driver) -> bool:
        """Закрытие всплывающего окна (попапа), если оно есть."""
        return BannerHandler.kill_all_banners(driver)


# ========== Функции для работы с корзиной ==========

class CartHelper:
    """Класс-помощник для работы с корзиной."""
    
    @staticmethod
    def get_cart_counter(driver) -> int:
        """Получение значения счетчика корзины."""
        from test.ui_test_data import Selectors
        try:
            counter_element = driver.find_element(*Selectors.Header.CART_COUNTER)
            text = counter_element.text.strip()
            if text and text.isdigit():
                return int(text)
            return 0
        except (NoSuchElementException, ValueError):
            return 0
    
    @staticmethod
    def find_and_click_buy_button(driver, book_name: str) -> bool:
        """Поиск и клик по кнопке 'Купить' с обработкой баннеров."""
        from test.ui_test_data import Selectors
        
        BannerHandler.kill_all_banners(driver)
        time.sleep(1)
        
        selectors = [
            Selectors.Search.FIRST_BUY_BUTTON,
            Selectors.Search.BUY_BUTTON,
            (By.XPATH, "//button[contains(text(), 'Купить')]"),
            (By.XPATH, "//button[contains(@class, 'product-buttons__main-action')]"),
            (By.CSS_SELECTOR, "button[data-testid-button-mini-product-card='canBuy']"),
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(*selector)
                if elements:
                    for elem in elements:
                        if elem.is_displayed():
                            print(f"  Кнопка найдена по селектору: {selector}")
                            scroll_to_element(driver, elem)
                            
                            if safe_click(driver, elem):
                                print(f"  Книга '{book_name}' добавлена в корзину")
                                return True
            except:
                continue
        
        # JavaScript поиск как fallback
        try:
            js_script = """
            var buttons = document.querySelectorAll('button');
            for(var i=0; i<buttons.length; i++) {
                if(buttons[i].textContent.includes('Купить')) {
                    buttons[i].click();
                    return true;
                }
            }
            return false;
            """
            result = driver.execute_script(js_script)
            if result:
                print(f"  Книга '{book_name}' добавлена через JavaScript")
                return True
        except:
            pass
        
        return False
    
    @staticmethod
    def find_increment_button(driver):
        """Поиск кнопки увеличения количества в корзине."""
        from test.ui_test_data import Selectors
        
        selectors = [
            Selectors.Cart.INCREMENT_BUTTON,
            (By.CSS_SELECTOR, ".counter__button--plus"),
            (By.XPATH, "//button[contains(@class, 'increment')]"),
            (By.XPATH, "//button[contains(text(), '+')]"),
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(*selector)
                if elements and elements[0].is_displayed():
                    return elements[0]
            except:
                continue
        return None
    
    @staticmethod
    def is_cart_empty(driver) -> bool:
        """Проверка, что корзина пуста."""
        from test.ui_test_data import Selectors
        
        try:
            cart_items = driver.find_elements(*Selectors.Cart.CART_ITEM)
            empty_message = driver.find_elements(*Selectors.Cart.EMPTY_CART_MESSAGE)
            restore_buttons = driver.find_elements(By.XPATH, "//div[contains(text(), 'Восстановить корзину')]")
            
            return len(cart_items) == 0 or empty_message or restore_buttons
        except:
            return False
    
    @staticmethod
    def wait_for_cart_empty(driver, timeout=30) -> bool:
        """Ожидание очистки корзины."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if CartHelper.is_cart_empty(driver):
                    print(f"  Корзина опустела через {time.time() - start_time:.1f} сек")
                    return True
                time.sleep(1)
            except:
                time.sleep(1)
        
        return CartHelper.is_cart_empty(driver)


# ========== Функции для работы с поиском ==========

class SearchHelper:
    """Класс-помощник для работы с поиском."""
    
    @staticmethod
    def search_book(driver, query: str) -> bool:
        """Поиск книги по запросу."""
        from test.ui_test_data import Selectors
        
        search_input = wait_and_find_element(driver, Selectors.Header.SEARCH_INPUT)
        if not search_input:
            return False
        
        search_input.clear()
        search_input.send_keys(query)
        search_input.submit()
        print(f"  Поиск: {query}")
        time.sleep(3)
        return True


# ========== Общие утилиты ==========

def count_digits_in_string(text: str) -> int:
    """Подсчет количества цифр в строке."""
    if not text:
        return 0
    return len(re.findall(r'\d', text))


def extract_number_from_text(text: str) -> Optional[int]:
    """Извлечение числа из текста."""
    numbers = re.findall(r'\d+', text)
    return int(numbers[0]) if numbers else None


def take_screenshot(driver, name: str = "screenshot") -> str:
    """Создание скриншота и прикрепление к Allure отчету."""
    screenshot_path = f"{name}.png"
    driver.save_screenshot(screenshot_path)
    allure.attach.file(screenshot_path, name=name, attachment_type=allure.attachment_type.PNG)
    return screenshot_path


def generate_test_report(results: List[Dict], title: str = "Отчет") -> str:
    """Генерация текстового отчета по результатам тестов."""
    passed = [r for r in results if r.get("passed", False)]
    failed = [r for r in results if not r.get("passed", False)]
    
    report = "="*80 + "\n"
    report += f"{title:^80}\n"
    report += "="*80 + "\n\n"
    
    report += f"Всего проверок: {len(results)}\n"
    report += f"  ✅ Успешно: {len(passed)}\n"
    report += f"  ❌ Ошибок: {len(failed)}\n\n"
    
    if results and "description" in results[0]:
        report += "-"*80 + "\n"
        report += "ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ:\n"
        report += "-"*80 + "\n"
        
        for r in results:
            status = "✅ УСПЕХ" if r.get("passed") else "❌ ОШИБКА"
            report += f"\n{status} | {r.get('description', '')}\n"
            for key, value in r.items():
                if key not in ["passed", "description"]:
                    report += f"  {key}: {value}\n"
    
    if failed:
        report += "\n" + "!"*80 + "\n"
        report += "СПИСОК ОШИБОК:\n"
        for r in failed:
            report += f"  • {r.get('description', '')}\n"
    
    report += "\n" + "="*80 + "\n"
    return report