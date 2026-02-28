import time
from selenium.webdriver.common.by import By
from tests.base_test import BaseTest

class LoginPage(BaseTest):
    """Класс для работы со страницей авторизации"""
    
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://www.chitai-gorod.ru"
    
    def find_login_button(self):
        """Поиск кнопки 'Войти'"""
        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".header-controls__btn")
        for button in buttons:
            if button.text == "Войти":
                print("✅ Нашли кнопку входа")
                return button
        return None
    
    def find_phone_input(self):
        """Поиск поля для ввода номера телефона"""
        phone_selectors = [
            "input[type='tel']",
            "input[inputmode='tel']",
            "input[placeholder*='телефон']"
        ]
        
        for selector in phone_selectors:
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed():
                    print(f"✅ Нашли поле телефона по селектору: {selector}")
                    return element
        return None
    
    def find_get_code_button(self):
        """Поиск кнопки 'Получить код'"""
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if button.is_displayed() and button.text and "получить код" in button.text.lower():
                print(f"✅ Нашли кнопку: '{button.text}'")
                return button
        return None
    
    def wait_for_redirect_back(self, timeout=60):
        """Ожидание возврата на сайт Читай-город"""
        print("Ожидаем возврата на сайт Читай-город после авторизации...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            current_url = self.driver.current_url
            if "chitai-gorod.ru" in current_url and "profile" in current_url:
                print(f"✅ Вернулись на сайт: {current_url}")
                return True
            time.sleep(2)
        
        print("⚠️ Не дождались возврата на сайт")
        return False
    
    def login(self, phone_number):
        """Полный процесс авторизации"""
        # Нажимаем кнопку "Войти"
        login_button = self.find_login_button()
        if not login_button:
            raise Exception("Кнопка 'Войти' не найдена")
        login_button.click()
        time.sleep(2)
        print("✅ Нажата кнопка 'Войти'")
        
        # Вводим номер телефона
        phone_input = self.find_phone_input()
        if not phone_input:
            raise Exception("Поле для ввода телефона не найдено")
        phone_input.clear()
        time.sleep(0.5)
        phone_input.send_keys(phone_number)
        time.sleep(1)
        print(f"✅ Введен номер телефона: {phone_number}")
        
        # Нажимаем кнопку "Получить код"
        get_code_button = self.find_get_code_button()
        if not get_code_button:
            raise Exception("Кнопка 'Получить код' не найдена")
        get_code_button.click()
        time.sleep(3)
        print("✅ Нажата кнопка 'Получить код'")
        
        # Инструкция для ручного ввода
        print("\n" + "="*70)
        print("🔐 РУЧНОЙ ВВОД SMS-КОДА")
        print("="*70)
        print("1. Вы будете перенаправлены на сайт Т-Банка")
        print("2. Введите полученный SMS-код вручную")
        print("3. После входа автоматически вернитесь на сайт Читай-город")
        print("="*70)
        print("\n⏳ Ожидаем возврата на сайт Читай-город...\n")
        
        # Ждем возврата на сайт
        if not self.wait_for_redirect_back():
            print("⚠️ Время ожидания истекло. Проверьте, выполнен ли вход вручную.")