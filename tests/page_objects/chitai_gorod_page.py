import allure
import time
from selenium.webdriver.common.by import By
from tests.page_objects.base_page import BasePage
from tests.page_objects.locators import PersonalDataPageLocators

class ChitaiGorodPage(BasePage):
    """Класс для работы со страницей Читай-город"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.base_url = "https://www.chitai-gorod.ru"
    
    @allure.step("Открыть страницу личных данных")
    def open_personal_data_page(self):
        """Открытие страницы личных данных"""
        self.driver.get(f"{self.base_url}/profile/personal-data")
        time.sleep(2)
    
    @allure.step("Авторизоваться с токеном")
    def login_with_token(self, token):
        """Авторизация с использованием токена"""
        # Очищаем localStorage перед установкой нового токена
        self.driver.execute_script("localStorage.clear();")
        time.sleep(1)
        
        # Устанавливаем токен
        script = f"""
        localStorage.setItem('accessToken', '{token}');
        localStorage.setItem('token_type', 'Bearer');
        console.log('Token set in localStorage');
        """
        self.driver.execute_script(script)
        time.sleep(1)
        
        # Проверяем, что токен установлен
        token_check = self.driver.execute_script("return localStorage.getItem('accessToken');")
        print(f"Токен установлен: {token_check is not None}")
        
        # Обновляем страницу
        self.driver.refresh()
        time.sleep(3)
    
    @allure.step("Найти поле Фамилия")
    def find_surname_field(self):
        """Поиск поля Фамилия на странице"""
        # Сначала пробуем найти по значению
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "input[value='Гашимова']")
            if elements:
                print("Нашли поле по значению 'Гашимова'")
                return elements[0]
        except:
            pass
        
        # Пробуем найти по ID (как в вашем примере)
        try:
            element = self.driver.find_element(By.ID, "v-0-65-0")
            print("Нашли поле по ID: v-0-65-0")
            return element
        except:
            pass
        
        # Пробуем найти по частичному ID
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "input[id^='v-0-']")
            if elements:
                print(f"Нашли поле по частичному ID: {elements[0].get_attribute('id')}")
                return elements[0]
        except:
            pass
        
        # Пробуем найти по классу
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "input.chg-app-input__control")
            for element in elements:
                value = element.get_attribute('value')
                print(f"Поле с классом chg-app-input__control, value={value}")
                if value == 'Гашимова':
                    return element
        except:
            pass
        
        # Если ничего не нашли, ищем среди всех input
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        print(f"Всего input полей: {len(inputs)}")
        
        for i, input_field in enumerate(inputs):
            input_id = input_field.get_attribute('id')
            input_value = input_field.get_attribute('value')
            input_placeholder = input_field.get_attribute('placeholder')
            input_class = input_field.get_attribute('class')
            
            print(f"Input {i}: id={input_id}, value={input_value}, placeholder={input_placeholder}, class={input_class}")
            
            # Проверяем по значению
            if input_value == 'Гашимова':
                print(f"Нашли поле по значению 'Гашимова' на позиции {i}")
                return input_field
            
            # Проверяем по placeholder
            if input_placeholder and 'фамили' in input_placeholder.lower():
                print(f"Нашли поле по placeholder на позиции {i}")
                return input_field
        
        self.take_screenshot("surname_field_not_found")
        raise Exception("Поле Фамилия не найдено на странице")
    
    @allure.step("Ввести фамилию: {surname}")
    def enter_surname(self, surname):
        """Ввод значения в поле Фамилия"""
        surname_field = self.find_surname_field()
        surname_field.clear()
        time.sleep(0.5)
        surname_field.send_keys(surname)
        time.sleep(1)
    
    @allure.step("Сохранить изменения")
    def save_changes(self):
        """Нажатие на кнопку сохранения"""
        # Пробуем найти кнопку сохранения
        selectors = [
            "button[type='submit']",
            "button.chg-button",
            "button:contains('Сохранить')",
            "button.btn-primary",
            ".profile-form button",
            "form button"
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    # Пробуем найти кнопку с текстом "Сохранить"
                    for element in elements:
                        if 'сохранить' in element.text.lower():
                            element.click()
                            print("Нажали кнопку Сохранить")
                            time.sleep(2)
                            return
                    
                    # Если не нашли по тексту, нажимаем первую
                    elements[0].click()
                    print(f"Нажали кнопку по селектору {selector}")
                    time.sleep(2)
                    return
            except:
                continue
        
        self.take_screenshot("save_button_not_found")
        raise Exception("Кнопка сохранения не найдена")
    
    @allure.step("Получить текущее значение поля Фамилия")
    def get_surname_value(self):
        """Получение текущего значения поля Фамилия"""
        surname_field = self.find_surname_field()
        return surname_field.get_attribute('value')
    
    @allure.step("Проверить наличие сообщения об успехе")
    def is_success_message_present(self):
        """Проверка наличия сообщения об успешном сохранении"""
        selectors = [
            ".chg-notification__success",
            ".success-message",
            "[class*='success']",
            ".alert-success",
            ".notification-success"
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and elements[0].is_displayed():
                    print(f"Нашли сообщение об успехе по селектору {selector}")
                    return True
            except:
                continue
        
        return False
    
    @allure.step("Проверить наличие сообщения об ошибке")
    def is_error_message_present(self):
        """Проверка наличия сообщения об ошибке валидации"""
        selectors = [
            ".chg-input__error",
            ".error-message",
            "[class*='error']",
            ".alert-danger",
            ".notification-error",
            ".invalid-feedback"
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and elements[0].is_displayed():
                    print(f"Нашли сообщение об ошибке по селектору {selector}")
                    return True
            except:
                continue
        
        return False
    
    @allure.step("Ввести фамилию и сохранить: {surname}")
    def enter_surname_and_save(self, surname):
        """Ввод фамилии и сохранение"""
        self.enter_surname(surname)
        self.save_changes()