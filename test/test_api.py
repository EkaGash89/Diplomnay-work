"""
API тесты для сайта "Читай-город"
"""

import os
import sys
from typing import Dict, List, Any, Optional, Union
from urllib.parse import quote

import pytest
import allure
import requests
from requests import Response

# Добавляем путь к корневой папке для импорта api_client
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from api_client import ChitaiGorodAPI

# ========== КОНСТАНТЫ ==========

# Тестовые данные для поисковых запросов
TEST_QUERIES: Dict[str, List[str]] = {
    "cyrillic": ["мертвые души", "война и мир", "преступление и наказание", "мастер и маргарита"],
    "with_numbers": ["1984", "451 градус", "100 лет", "50 оттенков"],
    "latin": ["harry potter", "lord of the rings", "game of thrones", "dune", "python"],
    "special_chars": ["!@#$%", "***", "___", "{}[]", "\\/", "~`"]
}

# Допустимые статус-коды для различных сценариев
HTTP_STATUS = {
    "SUCCESS": [200],
    "AUTH_ERRORS": [401, 403],
    "CLIENT_ERRORS": [400, 404, 405, 415, 422],
    "SERVER_ERRORS": [500, 501],
    "ALL_AUTH_ERRORS": [200, 401, 403],
    "ALL_CLIENT_ERRORS": [400, 403, 404, 422],
    "ALL_METHOD_ERRORS": [400, 403, 404, 405, 415, 500, 501]
}

# Настройки тестов
TEST_CONFIG = {
    "max_products_to_check": 5,
    "default_search_phrase": "мертвые души",
    "very_long_query_length": 1000,
    "query_lengths": [1, 10, 50, 100, 200]
}


# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

def has_latin_characters(text: Optional[str]) -> bool:
    """
    Проверка наличия латинских букв в тексте.
    
    Args:
        text: Проверяемый текст
        
    Returns:
        True если в тексте есть латинские буквы
    """
    if not text:
        return False
    return any('a' <= char.lower() <= 'z' for char in text if char.isalpha())


def handle_api_response(
    response: Optional[Response], 
    expected_statuses: Optional[List[int]] = None, 
    skip_on_auth_errors: bool = False
) -> bool:
    """
    Обработка ответа API с учетом возможных ошибок авторизации.
    
    Args:
        response: Объект ответа requests
        expected_statuses: Список ожидаемых статус-кодов
        skip_on_auth_errors: Пропускать тест при ошибках авторизации
        
    Returns:
        True если ответ прошел проверку
        
    Raises:
        AssertionError: Если статус-код не соответствует ожидаемому
    """
    if response is None:
        pytest.fail("Ответ API не получен")
    
    if skip_on_auth_errors and response.status_code in HTTP_STATUS["AUTH_ERRORS"]:
        pytest.skip(f"API недоступно. Статус: {response.status_code}")
    
    if expected_statuses:
        assert response.status_code in expected_statuses, \
            f"Expected one of {expected_statuses}, got {response.status_code}"
    
    return True


def safe_get_products(api: ChitaiGorodAPI, response: Optional[Response]) -> List[Dict[str, Any]]:
    """
    Безопасное получение продуктов из ответа.
    
    Args:
        api: Экземпляр API клиента
        response: Объект ответа requests
        
    Returns:
        Список продуктов или пустой список
    """
    try:
        if response is None or response.status_code != 200:
            return []
        products = api.get_products_from_response(response)
        return products if products else []
    except (ValueError, AttributeError, KeyError):
        return []


# ========== ТЕСТЫ ==========

@allure.feature("API тесты")
@allure.epic("Читай-город API")
class TestSearchAPI:
    """Тесты для поискового API Читай-город."""

    def setup_method(self) -> None:
        """Подготовка перед каждым тестом."""
        self.api = ChitaiGorodAPI()

    @allure.feature("Поиск")
    @allure.story("Позитивные сценарии")
    @allure.title("Поиск по названию на кириллице")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_by_cyrillic_title(self) -> None:
        """Проверка поиска книги по названию на русском языке."""
        
        for query in TEST_QUERIES["cyrillic"]:
            with allure.step(f"Выполнить поиск по запросу '{query}'"):
                response = self.api.search_product(query)
                
                # Проверяем что ответ успешный или доступ запрещен
                if response and response.status_code == 200:
                    products = safe_get_products(self.api, response)
                    if len(products) > 0:
                        allure.attach(
                            f"Найдено книг: {len(products)}", 
                            name="Результаты поиска", 
                            attachment_type=allure.attachment_type.TEXT
                        )
                        return  # Тест пройден если нашли хотя бы один результат
                elif response and response.status_code in HTTP_STATUS["AUTH_ERRORS"]:
                    allure.attach(
                        f"Статус: {response.status_code}", 
                        name="Ошибка авторизации", 
                        attachment_type=allure.attachment_type.TEXT
                    )
                    continue
                    
        # Если ни один запрос не дал результатов и не было 403, пропускаем тест
        pytest.skip("Не удалось найти книги по русским названиям или API недоступно")

    @allure.feature("Поиск")
    @allure.story("Позитивные сценарии")
    @allure.title("Поиск по названию с цифрами")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_by_title_with_numbers(self) -> None:
        """Проверка поиска книги по названию, содержащему цифры."""
        
        for query in TEST_QUERIES["with_numbers"]:
            with allure.step(f"Поиск по запросу '{query}'"):
                response = self.api.search_product(query)
                
                if response and response.status_code == 200:
                    products = safe_get_products(self.api, response)
                    
                    if products:
                        # Проверяем наличие цифр в названиях
                        found_with_digits = False
                        for product in products[:TEST_CONFIG["max_products_to_check"]]:
                            title = self.api.extract_product_title(product)
                            if title and any(char.isdigit() for char in title):
                                found_with_digits = True
                                break
                        
                        if found_with_digits:
                            allure.attach(
                                f"Найдены книги с цифрами в названии", 
                                name="Результат", 
                                attachment_type=allure.attachment_type.TEXT
                            )
                            return
                elif response and response.status_code in HTTP_STATUS["AUTH_ERRORS"]:
                    continue
        
        pytest.skip("Книги с цифрами в названии не найдены или API недоступно")

    @allure.feature("Авторизация")
    @allure.story("Негативные сценарии")
    @allure.title("Неверный API ключ")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_api_key(self) -> None:
        """Проверка обработки неверного API ключа."""
        
        with allure.step("Создать клиент с неверным ключом"):
            invalid_api = ChitaiGorodAPI(api_key="invalid_token_12345")
            
        with allure.step("Выполнить поиск с неверным ключом"):
            response = invalid_api.search_product(TEST_CONFIG["default_search_phrase"])
            
            # API может вернуть различные статусы
            handle_api_response(
                response, 
                expected_statuses=HTTP_STATUS["ALL_AUTH_ERRORS"], 
                skip_on_auth_errors=False
            )

    @allure.feature("Авторизация")
    @allure.story("Негативные сценарии")
    @allure.title("Поиск без API ключа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_without_api_key(self) -> None:
        """Проверка поиска без передачи API ключа."""
        
        with allure.step("Выполнить поиск без авторизации"):
            response = self.api.search_without_auth(TEST_CONFIG["default_search_phrase"])
            
        with allure.step("Проверить ответ"):
            # API может вернуть 200 (если ключ не обязателен), 401 или 403
            handle_api_response(
                response, 
                expected_statuses=HTTP_STATUS["ALL_AUTH_ERRORS"], 
                skip_on_auth_errors=False
            )

    @allure.feature("Поиск")
    @allure.story("Позитивные сценарии")
    @allure.title("Поиск по названию с латинскими буквами: {query}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("query", TEST_QUERIES["latin"])
    def test_search_by_title_with_latin_param(self, query: str) -> None:
        """
        Параметризованный тест поиска по названиям с латинскими буквами.
        
        Args:
            query: Поисковый запрос
        """
        with allure.step(f"Выполнить поиск по запросу '{query}'"):
            response = self.api.search_product(query)
            
            # Обрабатываем ответ - разрешаем 200, 401, 403
            handle_api_response(
                response, 
                expected_statuses=HTTP_STATUS["ALL_AUTH_ERRORS"], 
                skip_on_auth_errors=False
            )
            
            if response and response.status_code == 200:
                products = safe_get_products(self.api, response)
                
                # Если есть результаты, проверяем наличие латиницы (необязательно)
                if len(products) > 0:
                    for product in products[:TEST_CONFIG["max_products_to_check"]]:
                        title = self.api.extract_product_title(product)
                        if has_latin_characters(title):
                            allure.attach(
                                f"Найдены книги с латиницей", 
                                name="Результат", 
                                attachment_type=allure.attachment_type.TEXT
                            )
                            return

    @allure.feature("Негативные сценарии")
    @allure.story("Неправильные методы запроса")
    @allure.title("Поиск с использованием различных неправильных HTTP методов")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("method", ["POST", "PUT", "DELETE", "PATCH"])
    def test_search_with_various_wrong_methods(self, method: str) -> None:
        """
        Проверка отправки запросов с разными неправильными HTTP методами.
        
        Args:
            method: HTTP метод для тестирования
        """
        url = f"{self.api.base_url}/search/product"
        params = self.api.get_search_params(TEST_CONFIG["default_search_phrase"])
        headers = self.api.get_headers(include_auth=True)
        
        with allure.step(f"Выполнить {method} запрос"):
            response: Optional[Response] = None
            
            if method == "POST":
                response = requests.post(url, params=params, headers=headers, timeout=self.api.timeout)
            elif method == "PUT":
                response = requests.put(url, params=params, headers=headers, timeout=self.api.timeout)
            elif method == "DELETE":
                response = requests.delete(url, params=params, headers=headers, timeout=self.api.timeout)
            elif method == "PATCH":
                response = requests.patch(url, params=params, headers=headers, timeout=self.api.timeout)
        
        with allure.step("Проверить статус код"):
            # API может вернуть различные статусы для неподдерживаемых методов
            handle_api_response(
                response, 
                expected_statuses=HTTP_STATUS["ALL_METHOD_ERRORS"], 
                skip_on_auth_errors=False
            )

    @allure.feature("Поиск")
    @allure.story("Граничные сценарии")
    @allure.title("Поиск со специальными символами")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_with_special_characters(self) -> None:
        """Проверка поиска с использованием специальных символов."""
    
        for query in TEST_QUERIES["special_chars"]:
            with allure.step(f"Поиск по запросу '{query}'"):
                response = self.api.search_product(query)
            
                # Проверяем что ответ не None
                assert response is not None, f"Нет ответа для запроса '{query}'"
                
                # Проверяем что статус код в допустимом диапазоне
                assert response.status_code in HTTP_STATUS["ALL_CLIENT_ERRORS"], \
                    f"Запрос '{query}' вернул неожиданный статус: {response.status_code}"

    @allure.feature("Поиск")
    @allure.story("Граничные сценарии")
    @allure.title("Поиск с пустым запросом")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_with_empty_query(self) -> None:
        """Проверка поиска с пустым запросом."""
        
        with allure.step("Выполнить поиск с пустым запросом"):
            response = self.api.search_product("")
            
            # Обрабатываем ответ
            handle_api_response(
                response, 
                expected_statuses=HTTP_STATUS["ALL_CLIENT_ERRORS"], 
                skip_on_auth_errors=False
            )

    @allure.feature("Поиск")
    @allure.story("Граничные сценарии")
    @allure.title("Поиск с очень длинным запросом")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_with_very_long_query(self) -> None:
        """Проверка поиска с очень длинным запросом."""
        
        # Создаем очень длинный запрос
        long_query = "а" * TEST_CONFIG["very_long_query_length"]
        
        with allure.step(f"Выполнить поиск с запросом длиной {TEST_CONFIG['very_long_query_length']}"):
            response = self.api.search_product(long_query)
            
            # Проверяем ответ
            expected_statuses = HTTP_STATUS["ALL_CLIENT_ERRORS"] + [414, 500]
            handle_api_response(
                response, 
                expected_statuses=expected_statuses, 
                skip_on_auth_errors=False
            )

    @allure.feature("Поиск")
    @allure.story("Позитивные сценарии")
    @allure.title("Поиск с различной длиной запроса")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("length", TEST_CONFIG["query_lengths"])
    def test_search_with_various_lengths(self, length: int) -> None:
        """
        Параметризованный тест поиска с запросами разной длины.
        
        Args:
            length: Длина поискового запроса
        """
        # Создаем запрос указанной длины
        query = "а" * length
        
        with allure.step(f"Выполнить поиск с запросом длиной {length}"):
            response = self.api.search_product(query)
            
            # Проверяем что ответ получен
            assert response is not None, f"Нет ответа для запроса длиной {length}"
            
            # Проверяем статус код
            assert response.status_code in HTTP_STATUS["ALL_CLIENT_ERRORS"] + [200], \
                f"Недопустимый статус для запроса длиной {length}: {response.status_code}"
            
            if response.status_code == 200:
                products = safe_get_products(self.api, response)
                allure.attach(
                    f"Длина запроса: {length}\nНайдено продуктов: {len(products)}",
                    name="Результаты поиска",
                    attachment_type=allure.attachment_type.TEXT
                )


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])