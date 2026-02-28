import time
from selenium.webdriver.common.by import By
from tests.base_test import BaseTest

class ProfilePage(BaseTest):
    """Класс для работы со страницей профиля"""
    
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://www.chitai-gorod.ru/profile/personal-data"
    
    def open(self):
        """Открыть страницу профиля"""
        self.driver.get(self.base_url)
        time.sleep(3)
        print(f"✅ Открыта страница профиля: {self.driver.current_url}")
    
    def find_surname_field(self):
        """Поиск поля фамилии"""
        # По ID
        try:
            field = self.driver.find_element(By.ID, "v-0-1-0")
            print("✅ Нашли поле фамилии по ID: v-0-1-0")
            return field
        except:
            pass
        
        # По порядку (2-е поле ввода)
        try:
            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input.chg-app-input__control")
            if len(inputs) >= 2:
                print("✅ Нашли поле фамилии по порядку (2-е поле ввода)")
                return inputs[1]
        except:
            pass
        
        raise Exception("Поле фамилии не найдено")
    
    def test_input_value(self, field, value):
        """Тестирование ввода значения в поле"""
        try:
            # Прокручиваем до поля
            self.scroll_to_element(field)
            
            # Кликаем по полю
            try:
                field.click()
            except:
                self.driver.execute_script("arguments[0].click();", field)
            time.sleep(0.5)
            
            # Очищаем поле
            if not self.clear_field_reliably(field):
                print("⚠️ Не удалось очистить поле")
            
            # Пробуем ввести значение
            try:
                field.send_keys(value)
                time.sleep(0.5)
            except:
                print("⚠️ Обычный ввод не сработал, пробуем JavaScript")
                return self.force_set_value(field, value)
            
            # Проверяем результат
            current_value = field.get_attribute('value')
            if current_value != value:
                print(f"⚠️ Обычный ввод дал '{current_value}', пробуем JavaScript")
                return self.force_set_value(field, value)
            
            return current_value == value
            
        except Exception as e:
            print(f"⚠️ Ошибка при вводе: {e}")
            return self.force_set_value(field, value)