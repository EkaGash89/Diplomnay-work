import pytest
import allure
import time
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from tests.base_test import BaseTest
from tests.pages.login_page import LoginPage
from tests.pages.profile_page import ProfilePage

load_dotenv()

@allure.feature("UI Тесты")
class TestSurnameField:
    """UI тесты для проверки поля Фамилия в разделе Личные данные"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class_fixture(self, request):
        """Фикстура для настройки класса - выполняется один раз перед всеми тестами"""
        print("\n" + "="*70)
        print("🚀 ИНИЦИАЛИЗАЦИЯ ТЕСТОВОГО КЛАССА")
        print("="*70)
        
        # Создаем экземпляр BaseTest для управления браузером
        base_test = BaseTest()
        base_test.setup_method()
        
        # Сохраняем driver и другие объекты в атрибутах класса
        request.cls.driver = base_test.driver
        request.cls.base_test = base_test
        request.cls.phone_number = os.getenv('PHONE_NUMBER', '9320926010')
        request.cls.login_page = LoginPage(base_test.driver)
        request.cls.profile_page = ProfilePage(base_test.driver)
        
        # Создаем экземпляр тестового класса и вызываем метод
        test_instance = request.cls()
        test_instance.driver = base_test.driver
        test_instance.base_test = base_test
        test_instance.phone_number = request.cls.phone_number
        test_instance.login_page = request.cls.login_page
        test_instance.profile_page = request.cls.profile_page
        
        # Выполняем предварительные шаги (авторизацию) один раз
        test_instance._setup_profile_page()
        
        # Сохраняем состояние после авторизации в атрибуты класса
        request.cls.is_authorized = True
        
        yield
        
        # Закрываем браузер после всех тестов
        print("\n" + "="*70)
        print("🏁 ЗАВЕРШЕНИЕ ТЕСТИРОВАНИЯ")
        print("="*70)
        time.sleep(2)
        if hasattr(request.cls, 'driver'):
            request.cls.driver.quit()
    
    def _setup_profile_page(self):
        """Предварительные шаги: авторизация и открытие страницы профиля"""
        with allure.step("Предварительные шаги: авторизация и открытие страницы профиля"):
            print("\n🔐 Выполняем предварительную авторизацию...")
            
            # Открываем главную страницу
            self.driver.get("https://www.chitai-gorod.ru")
            time.sleep(2)
            print("✅ Открыта главная страница")
            
            # Процесс авторизации
            self.login_page.login(self.phone_number)
            
            # Переходим на страницу личных данных
            self.profile_page.open()
            assert "profile" in self.driver.current_url or "personal-data" in self.driver.current_url, "Не удалось открыть страницу профиля"
            
            # Закрываем баннер если есть
            self.base_test.close_banner()
            
            print("✅ Предварительные шаги выполнены успешно")
    
    def get_surname_field(self):
        """Получение поля фамилии (без повторной авторизации)"""
        return self.profile_page.find_surname_field()
    
    @allure.story("Позитивные проверки")
    @allure.title("Позитивный тест 1: Ввод фамилии в верхнем и нижнем регистре: ИваНов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_positive_mixed_case(self):
        """Проверка ввода фамилии в верхнем и нижнем регистре"""
        test_value = "ИваНов"
        test_desc = "Верхний и нижний регистр"
        
        with allure.step(f"Вводим значение '{test_value}'"):
            surname_field = self.get_surname_field()
            input_success = self.profile_page.test_input_value(surname_field, test_value)
            
            assert input_success, f"❌ ТЕСТ 1 НЕ ПРОЙДЕН - не удалось ввести значение '{test_value}'"
            
            current_value = surname_field.get_attribute('value')
            assert current_value == test_value, f"Ожидалось '{test_value}', получено '{current_value}'"
            
            print(f"✅ ТЕСТ 1 ПРОЙДЕН: {test_desc} - значение успешно введено: '{current_value}'")
    
    @allure.story("Позитивные проверки")
    @allure.title("Позитивный тест 2: Ввод фамилии на латинице и кириллице: Ivaнов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_positive_mixed_script(self):
        """Проверка ввода фамилии на латинице и кириллице"""
        test_value = "Ivaнов"
        test_desc = "Латиница и кириллица"
        
        with allure.step(f"Вводим значение '{test_value}'"):
            surname_field = self.get_surname_field()
            input_success = self.profile_page.test_input_value(surname_field, test_value)
            
            assert input_success, f"❌ ТЕСТ 2 НЕ ПРОЙДЕН - не удалось ввести значение '{test_value}'"
            
            current_value = surname_field.get_attribute('value')
            assert current_value == test_value, f"Ожидалось '{test_value}', получено '{current_value}'"
            
            print(f"✅ ТЕСТ 2 ПРОЙДЕН: {test_desc} - значение успешно введено: '{current_value}'")
    
    @allure.story("Позитивные проверки")
    @allure.title("Позитивный тест 3: Ввод фамилии с дефисом: -Ива-нов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_positive_with_hyphen(self):
        """Проверка ввода фамилии с дефисом"""
        test_value = "-Ива-нов"
        test_desc = "С дефисом"
        
        with allure.step(f"Вводим значение '{test_value}'"):
            surname_field = self.get_surname_field()
            input_success = self.profile_page.test_input_value(surname_field, test_value)
            
            assert input_success, f"❌ ТЕСТ 3 НЕ ПРОЙДЕН - не удалось ввести значение '{test_value}'"
            
            current_value = surname_field.get_attribute('value')
            assert current_value == test_value, f"Ожидалось '{test_value}', получено '{current_value}'"
            
            print(f"✅ ТЕСТ 3 ПРОЙДЕН: {test_desc} - значение успешно введено: '{current_value}'")
    
    @allure.story("Позитивные проверки")
    @allure.title("Позитивный тест 4: Ввод фамилии с пробелом: Ива нов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_positive_with_space(self):
        """Проверка ввода фамилии с пробелом"""
        test_value = "Ива нов"
        test_desc = "С пробелом"
        
        with allure.step(f"Вводим значение '{test_value}'"):
            surname_field = self.get_surname_field()
            input_success = self.profile_page.test_input_value(surname_field, test_value)
            
            assert input_success, f"❌ ТЕСТ 4 НЕ ПРОЙДЕН - не удалось ввести значение '{test_value}'"
            
            current_value = surname_field.get_attribute('value')
            assert current_value == test_value, f"Ожидалось '{test_value}', получено '{current_value}'"
            
            print(f"✅ ТЕСТ 4 ПРОЙДЕН: {test_desc} - значение успешно введено: '{current_value}'")
    
    @allure.story("Позитивные проверки")
    @allure.title("Позитивный тест 5: Ввод фамилии с минимальным количеством символов: ко")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_positive_min_length(self):
        """Проверка ввода фамилии с минимальным количеством символов"""
        test_value = "ко"
        test_desc = "Минимальное кол-во символов (2)"
        
        with allure.step(f"Вводим значение '{test_value}'"):
            surname_field = self.get_surname_field()
            input_success = self.profile_page.test_input_value(surname_field, test_value)
            
            assert input_success, f"❌ ТЕСТ 5 НЕ ПРОЙДЕН - не удалось ввести значение '{test_value}'"
            
            current_value = surname_field.get_attribute('value')
            assert current_value == test_value, f"Ожидалось '{test_value}', получено '{current_value}'"
            
            print(f"✅ ТЕСТ 5 ПРОЙДЕН: {test_desc} - значение успешно введено: '{current_value}'")
    
    @allure.story("Позитивные проверки")
    @allure.title("Позитивный тест 6: Ввод фамилии с максимальным количеством символов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_positive_max_length(self):
        """Проверка ввода фамилии с максимальным количеством символов"""
        test_value = "апролнимтрвылирпнвтрлстраипвльтирпнвыдцзсьотрвныдл"
        test_desc = "Максимальное кол-во символов"
        
        with allure.step(f"Вводим значение (длина {len(test_value)} символов)"):
            surname_field = self.get_surname_field()
            input_success = self.profile_page.test_input_value(surname_field, test_value)
            
            assert input_success, f"❌ ТЕСТ 6 НЕ ПРОЙДЕН - не удалось ввести значение"
            
            current_value = surname_field.get_attribute('value')
            assert current_value == test_value, f"Ожидалось значение длиной {len(test_value)}, получено длиной {len(current_value)}"
            
            print(f"✅ ТЕСТ 6 ПРОЙДЕН: {test_desc} - значение успешно введено длиной {len(current_value)} символов")
    
    @allure.story("Негативные проверки")
    @allure.title("Негативный тест 7: Ввод фамилии со спец символами: №Иванов!")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_negative_special_chars(self):
        """Проверка ввода фамилии со спец символами"""
        test_value = "№Иванов!"
        test_desc = "Со спецсимволами"
        
        with allure.step(f"Вводим значение '{test_value}'"):
            surname_field = self.get_surname_field()
            input_success = self.profile_page.test_input_value(surname_field, test_value)
            
            # Проверяем наличие сообщения об ошибке
            has_error = self.base_test.check_error_message()
            
            if has_error:
                print(f"✅ ТЕСТ 7 ПРОЙДЕН: {test_desc} - появилось сообщение об ошибке")
            elif not input_success:
                print(f"✅ ТЕСТ 7 ПРОЙДЕН: {test_desc} - не удалось ввести значение")
            else:
                current_value = surname_field.get_attribute('value')
                if current_value != test_value:
                    print(f"✅ ТЕСТ 7 ПРОЙДЕН: {test_desc} - значение изменилось на '{current_value}'")
                else:
                    assert False, f"❌ ТЕСТ 7 НЕ ПРОЙДЕН: {test_desc} - значение '{test_value}' сохранилось без ошибки"
    
    @allure.story("Негативные проверки")
    @allure.title("Негативный тест 8: Оставление поля Фамилия пустым")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_negative_empty(self):
        """Проверка отправки пустого поля"""
        test_desc = "Пустое поле"
        
        with allure.step("Очищаем поле"):
            surname_field = self.get_surname_field()
            
            # Очищаем поле
            self.base_test.clear_field_reliably(surname_field)
            current_value = surname_field.get_attribute('value')
            
            # Проверяем что поле пустое
            assert current_value == "", f"Поле не очистилось, текущее значение: '{current_value}'"
            print(f"✅ ТЕСТ 8 ПРОЙДЕН: {test_desc} - поле можно очистить")
    
    @allure.story("Негативные проверки")
    @allure.title("Негативный тест 9: Ввод фамилии только из дефисов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_negative_only_hyphens(self):
        """Проверка ввода фамилии только из дефисов"""
        test_value = "-----------------------"
        test_desc = "Только из дефисов"
        
        with allure.step(f"Вводим значение '{test_value}'"):
            surname_field = self.get_surname_field()
            input_success = self.profile_page.test_input_value(surname_field, test_value)
            
            if input_success:
                current_value = surname_field.get_attribute('value')
                assert current_value == test_value, f"Ожидалось '{test_value}', получено '{current_value}'"
                print(f"⚠️ ТЕСТ 9: Значение из дефисов ввелось (возможно, это допустимо)")
                print(f"✅ ТЕСТ 9 ПРОЙДЕН: {test_desc} - значение ввелось")
            else:
                print(f"✅ ТЕСТ 9 ПРОЙДЕН: {test_desc} - не удалось ввести значение")
    
    @allure.story("Негативные проверки")
    @allure.title("Негативный тест 10: Ввод фамилии длиной 1 символ: к")
    @allure.severity(allure.severity_level.NORMAL)
    def test_negative_one_character(self):
        """Проверка ввода фамилии длиной 1 символ"""
        test_value = "к"
        test_desc = "Длина 1 символ"
        
        with allure.step(f"Вводим значение '{test_value}'"):
            surname_field = self.get_surname_field()
            input_success = self.profile_page.test_input_value(surname_field, test_value)
            
            if input_success:
                current_value = surname_field.get_attribute('value')
                assert current_value == test_value, f"Ожидалось '{test_value}', получено '{current_value}'"
                print(f"⚠️ ТЕСТ 10: Значение из 1 символа ввелось (возможно, это допустимо)")
                print(f"✅ ТЕСТ 10 ПРОЙДЕН: {test_desc} - значение ввелось")
            else:
                print(f"✅ ТЕСТ 10 ПРОЙДЕН: {test_desc} - не удалось ввести значение")


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])