"""
UI тесты для сайта "Читай-город"
"""

import os
import sys
import time
import pytest
import allure
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

# путь к корневой папке
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from test.ui_test_data import (
    BASE_URL, CART_URL, SALES_URL,
    PHONE_TEST_CASES, SEARCH_QUERIES,
    TEST_BOOKS, EXPECTED_VALUES, Selectors,
    TEST_CONFIG
)

from test.ui_helpers import (
    wait_and_find_element, wait_and_click,
    clear_and_send_keys, safe_click, scroll_to_element,
    count_digits_in_string, extract_number_from_text,
    generate_test_report, take_screenshot,
    BannerHandler, CartHelper, SearchHelper
)
from test.conftest import driver

load_dotenv()


@allure.feature("UI тесты")
@allure.epic("Читай-город")
class TestAuthorization:
    """Тесты авторизации на сайте."""

    @allure.story("Авторизация")
    @allure.title("Полная проверка валидации номера телефона")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_phone_validation_complete(self, driver):
        """Полный тест валидации поля ввода телефона."""
        
        with allure.step("Открыть главную страницу и открыть форму входа"):
            driver.get(BASE_URL)
            time.sleep(2)
            
            login_button = wait_and_find_element(driver, Selectors.Header.LOGIN_BUTTON)
            if login_button and login_button.is_displayed():
                login_button.click()
            else:
                wait_and_click(driver, Selectors.Header.LOGIN_ICON)
            time.sleep(2)

        phone_input = wait_and_find_element(driver, Selectors.Login.PHONE_INPUT)
        assert phone_input, "Поле ввода телефона не найдено"
        results = []

        for phone, expected, description in PHONE_TEST_CASES:
            with allure.step(f"Проверка: {description}"):
                # Очистка и ввод
                driver.execute_script("arguments[0].value = '';", phone_input)
                phone_input.clear()
                time.sleep(0.5)
                
                if phone:
                    phone_input.send_keys(phone)
                    time.sleep(2)
                else:
                    time.sleep(1)

                # Проверка кнопки
                get_code_button = wait_and_find_element(driver, Selectors.Login.GET_CODE_BUTTON)
                assert get_code_button, "Кнопка не найдена"
                
                is_enabled = get_code_button.is_enabled()
                button_class = get_code_button.get_attribute("class")
                is_disabled = "disabled" in button_class or "--disabled" in button_class
                actual_active = is_enabled and not is_disabled
                
                actual_value = phone_input.get_attribute("value") or "<пусто>"
                
                results.append({
                    "description": description,
                    "phone": phone or "<пусто>",
                    "cleaned": actual_value,
                    "digits": count_digits_in_string(actual_value),
                    "expected": "активна" if expected else "неактивна",
                    "actual": "активна" if actual_active else "неактивна",
                    "passed": actual_active == expected
                })

        report = generate_test_report(results, "ТЕСТИРОВАНИЕ ВАЛИДАЦИИ ТЕЛЕФОНА")
        allure.attach(report, "Отчет", allure.attachment_type.TEXT)
        
        failed = [r for r in results if not r["passed"]]
        assert len(failed) == 0, f"Найдено {len(failed)} ошибок"


@allure.feature("UI тесты")
@allure.epic("Читай-город")
class TestCart:
    """Тесты корзины."""

    @allure.story("Корзина")
    @allure.title("Добавление книги и проверка счетчика корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_add_book_to_cart(self, driver):
        """Тест добавления книги в корзину и проверки счетчика."""
        
        with allure.step("Открыть главную страницу"):
            driver.get(BASE_URL)
            time.sleep(3)
            print(f"\n=== ТЕСТ: ДОБАВЛЕНИЕ КНИГИ В КОРЗИНУ ===")
            BannerHandler.kill_all_banners(driver)

        initial_counter = CartHelper.get_cart_counter(driver)
        print(f"Начальный счетчик: {initial_counter}")

        with allure.step(f"Поиск книги: {SEARCH_QUERIES['griboedov']}"):
            assert SearchHelper.search_book(driver, SEARCH_QUERIES['griboedov']), "Ошибка поиска"
            BannerHandler.kill_all_banners(driver)

        with allure.step("Добавить книгу в корзину"):
            assert CartHelper.find_and_click_buy_button(driver, "Горе от ума"), "Не удалось добавить книгу"
            time.sleep(3)

        with allure.step("Проверить счетчик"):
            new_counter = CartHelper.get_cart_counter(driver)
            print(f"Новый счетчик: {new_counter}")
            
            assert new_counter > initial_counter, f"Счетчик не увеличился: {initial_counter} -> {new_counter}"
            print(f"\n✓ ТЕСТ ПРОЙДЕН: +{new_counter - initial_counter}")


@allure.feature("UI тесты")
@allure.epic("Читай-город")
class TestFilters:
    """Тесты фильтров и сортировки."""

    @allure.story("Фильтры и сортировка")
    @allure.title("Проверка фильтрации в разделе распродажа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sales_filters(self, driver):
        """Тест фильтрации в разделе распродажа."""
        
        with allure.step("Открыть раздел распродажа"):
            driver.get(SALES_URL)
            time.sleep(3)
            BannerHandler.kill_all_banners(driver)
        
        steps = [
            ("Выбрать категорию", Selectors.Filters.CATEGORY),
            ("Выбрать подкатегорию", Selectors.Filters.SUBCATEGORY),
            ("Ввести автора", Selectors.Filters.AUTHOR_INPUT, SEARCH_QUERIES["pushkin"]),
            ("Выбрать автора", Selectors.Filters.AUTHOR_SUGGESTION)
        ]
        
        for step in steps:
            with allure.step(step[0]):
                BannerHandler.kill_all_banners(driver)
                element = wait_and_find_element(driver, step[1])
                assert element, f"Элемент не найден: {step[1]}"
                
                scroll_to_element(driver, element)
                
                if len(step) > 2:  # Если есть текст для ввода
                    element.clear()
                    element.send_keys(step[2])
                    print(f"  Введен текст: {step[2]}")
                else:
                    assert safe_click(driver, element), f"Не удалось кликнуть: {step[0]}"
                    print(f"  {step[0]} выполнен")
                
                time.sleep(2)

        with allure.step("Проверить количество товаров после фильтрации"):
            BannerHandler.kill_all_banners(driver)
            time.sleep(3)  # Увеличим время ожидания для применения фильтров
            
            total_element = wait_and_find_element(driver, Selectors.Filters.PRODUCTS_TOTAL)
            assert total_element, "Счетчик не найден"
            
            actual_count = extract_number_from_text(total_element.text)
            print(f"  Найдено товаров после фильтрации: {actual_count}")
            
            # Проверяем, что количество товаров в разумном диапазоне (например, от 50 до 150)
            MIN_EXPECTED = 65
            MAX_EXPECTED = 85
            
            assert MIN_EXPECTED <= actual_count <= MAX_EXPECTED, \
                f"Количество товаров вне ожидаемого диапазона [{MIN_EXPECTED}, {MAX_EXPECTED}]: {actual_count}"
            
            # Сохраняем результат в отчет
            filter_info = (
                f"Количество после фильтрации: {actual_count}\n"
                f"Ожидаемый диапазон: [{MIN_EXPECTED}, {MAX_EXPECTED}]\n"
                f"Статус: {'✓ В диапазоне' if MIN_EXPECTED <= actual_count <= MAX_EXPECTED else '✗ Вне диапазона'}"
            )
            
            allure.attach(filter_info, name="Результаты фильтрации", 
                         attachment_type=allure.attachment_type.TEXT)
            
            print(f"\n✓ ТЕСТ ПРОЙДЕН: Найдено {actual_count} товаров (в диапазоне {MIN_EXPECTED}-{MAX_EXPECTED})")


@allure.feature("UI тесты")
@allure.epic("Читай-город")
class TestCartQuantityAndSum:
    """Тест: изменение количества товара и пересчет суммы."""

    @allure.story("Корзина")
    @allure.title("Добавление книги, увеличение количества и проверка пересчета суммы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_quantity_and_sum(self, driver):
        """Тест: добавление книги, увеличение количества и проверка пересчета суммы."""
        
        with allure.step("Открыть главную страницу"):
            driver.get(BASE_URL)
            time.sleep(3)
            print(f"\n=== ТЕСТ: ИЗМЕНЕНИЕ КОЛИЧЕСТВА И ПРОВЕРКА СУММЫ ===")
            BannerHandler.kill_all_banners(driver)
        
        with allure.step(f"Поиск книги: {SEARCH_QUERIES['master']}"):
            assert SearchHelper.search_book(driver, SEARCH_QUERIES['master']), "Ошибка поиска"
            BannerHandler.kill_all_banners(driver)
        
        with allure.step("Добавить книгу в корзину"):
            initial_counter = CartHelper.get_cart_counter(driver)
            print(f"  Начальный счетчик: {initial_counter}")
            
            assert CartHelper.find_and_click_buy_button(driver, "Мастер и Маргарита"), "Не удалось добавить книгу"
            time.sleep(3)
        
        with allure.step("Перейти в корзину"):
            driver.get(CART_URL)
            time.sleep(3)
            BannerHandler.kill_all_banners(driver)
        
        with allure.step(f"Увеличить количество товара"):
            increment_button = CartHelper.find_increment_button(driver)
            assert increment_button, "Кнопка '+' не найдена"
            
            quantity_input = driver.find_element(*Selectors.Cart.QUANTITY_INPUT)
            initial_quantity = int(quantity_input.get_attribute("value"))
            
            total_element = wait_and_find_element(driver, Selectors.Cart.TOTAL_SUM)
            initial_total = extract_number_from_text(total_element.text)
            
            totals = [initial_total]
            click_count = TEST_CONFIG["cart"]["click_count"]
            
            for i in range(click_count):
                BannerHandler.kill_all_banners(driver)
                assert safe_click(driver, increment_button), f"Не удалось нажать +"
                print(f"    Нажатие {i+1}/{click_count}")
                time.sleep(2)
                
                new_total = extract_number_from_text(total_element.text)
                totals.append(new_total)
                print(f"    Сумма: {new_total} ₽")
            
            new_quantity = int(quantity_input.get_attribute("value"))
            expected_quantity = initial_quantity + click_count
            
            assert new_quantity == expected_quantity, f"Ожидалось {expected_quantity}, получено {new_quantity}"
            
            for i in range(1, len(totals)):
                assert totals[i] > totals[i-1], f"Сумма не выросла на шаге {i}"
            
            print(f"\n✓ ТЕСТ ПРОЙДЕН: {initial_quantity} → {new_quantity}, сумма {totals[0]} → {totals[-1]} ₽")


@allure.feature("UI тесты")
@allure.epic("Читай-город")
class TestCartClear:
    """Тест: добавление товара и полная очистка корзины."""

    @allure.story("Корзина")
    @allure.title("Добавление товара и полная очистка корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_and_clear(self, driver):
        """Тест: добавление товара и полная очистка корзины."""
        
        with allure.step("Открыть главную страницу"):
            driver.get(BASE_URL)
            time.sleep(3)
            print(f"\n=== ТЕСТ: ДОБАВЛЕНИЕ ТОВАРА И ОЧИСТКА КОРЗИНЫ ===")
            BannerHandler.kill_all_banners(driver)
        
        book = TEST_BOOKS[0]
        
        with allure.step(f"Добавить книгу: {book['name']}"):
            assert SearchHelper.search_book(driver, book['query']), "Ошибка поиска"
            BannerHandler.kill_all_banners(driver)
            assert CartHelper.find_and_click_buy_button(driver, book['name']), "Не удалось добавить книгу"
            time.sleep(3)
        
        with allure.step("Перейти в корзину и проверить количество"):
            driver.get(CART_URL)
            time.sleep(3)
            BannerHandler.kill_all_banners(driver)
            
            cart_items = driver.find_elements(*Selectors.Cart.CART_ITEM)
            assert len(cart_items) == 1, f"Ожидался 1 товар, получено {len(cart_items)}"
            print(f"  ✓ В корзине {len(cart_items)} товар")
        
        with allure.step("Очистить корзину"):
            clear_button = wait_and_find_element(driver, Selectors.Cart.CLEAR_CART_BUTTON, timeout=5)
            
            if clear_button:
                scroll_to_element(driver, clear_button)
                assert safe_click(driver, clear_button), "Не удалось нажать 'Очистить'"
                print("  Нажата кнопка 'Очистить корзину'")
                time.sleep(2)
                
                confirm = wait_and_find_element(driver, Selectors.Cart.CONFIRM_CLEAR_BUTTON, timeout=3)
                if confirm:
                    assert safe_click(driver, confirm), "Не удалось подтвердить очистку"
                    print("  Подтверждена очистка")
                    time.sleep(3)
            else:
                # Удаление по одному
                delete_buttons = driver.find_elements(*Selectors.Cart.DELETE_BUTTON)
                for i, btn in enumerate(delete_buttons):
                    scroll_to_element(driver, btn)
                    assert safe_click(driver, btn), f"Не удалось удалить товар {i+1}"
                    time.sleep(1)
        
        with allure.step("Проверить что корзина пуста"):
            is_empty = CartHelper.wait_for_cart_empty(driver, TEST_CONFIG["cart"]["timeout"])
            
            cart_items = driver.find_elements(*Selectors.Cart.CART_ITEM)
            restore = driver.find_elements(*Selectors.Cart.RESTORE_BUTTON)
            
            print(f"  Товаров: {len(cart_items)}, Восстановление: {'да' if restore else 'нет'}")
            assert is_empty, "Корзина не опустела"
            print(f"\n✓ ТЕСТ ПРОЙДЕН: Корзина очищена")


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])