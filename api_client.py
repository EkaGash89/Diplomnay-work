"""API клиент для работы с сервисом Читай-город."""

import os
from typing import Any, Dict, List, Optional, Union

import requests
from dotenv import load_dotenv
from requests import Response

load_dotenv()


class ChitaiGorodAPI:
    """Клиент для работы с API Читай-город."""
    
    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Инициализация API клиента.
        
        Args:
            api_key: API ключ для авторизации
        """
        self.base_url: str = os.getenv('BASE_URL', 'https://www.chitai-gorod.ru')
        self.api_key: Optional[str] = api_key or os.getenv('API_KEY')
        self.timeout: int = int(os.getenv('TIMEOUT', '30'))
        self.default_city_id: str = "213"
        self.default_ab_test_group: str = "1"
    
    def get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        """
        Получение стандартных заголовков для запросов.
        
        Args:
            include_auth: Добавлять ли заголовок авторизации
            
        Returns:
            Словарь с заголовками
        """
        headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if include_auth and self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    def get_search_params(
        self, 
        phrase: str, 
        page: int = 1, 
        per_page: int = 60
    ) -> Dict[str, str]:
        """
        Получение стандартных параметров поиска.
        
        Args:
            phrase: Поисковый запрос
            page: Номер страницы
            per_page: Количество результатов на странице
            
        Returns:
            Словарь с параметрами запроса
        """
        return {
            "customerCityId": self.default_city_id,
            "products[page]": str(page),
            "products[per-page]": str(per_page),
            "phrase": phrase,
            "abTestGroup": self.default_ab_test_group
        }
    
    def extract_product_title(self, product: Dict[str, Any]) -> str:
        """
        Извлечение названия книги из продукта.
        
        Args:
            product: Данные продукта
            
        Returns:
            Название книги или пустая строка
        """
        if "attributes" in product:
            return product["attributes"].get("title", "")
        if "title" in product:
            return str(product.get("title", ""))
        return ""
    
    def search_product(
        self, 
        phrase: str, 
        page: int = 1, 
        per_page: int = 60
    ) -> Optional[Response]:
        """
        Поиск товаров по фразе.
        
        Args:
            phrase: Поисковый запрос
            page: Номер страницы
            per_page: Количество результатов на странице
            
        Returns:
            Response объект или None в случае ошибки
        """
        url = f"{self.base_url}/search/product"
        params = self.get_search_params(phrase, page, per_page)
        headers = self.get_headers(include_auth=True)
        
        try:
            response = requests.get(
                url, 
                params=params, 
                headers=headers,
                timeout=self.timeout
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None
    
    def search_without_auth(self, phrase: str) -> Optional[Response]:
        """
        Выполнение поиска без авторизации.
        
        Args:
            phrase: Поисковый запрос
            
        Returns:
            Response объект или None в случае ошибки
        """
        url = f"{self.base_url}/search/product"
        params = self.get_search_params(phrase)
        headers = self.get_headers(include_auth=False)
        
        try:
            response = requests.get(
                url, 
                params=params, 
                headers=headers,
                timeout=self.timeout
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None
    
    def get_products_from_response(self, response: Optional[Response]) -> List[Dict[str, Any]]:
        """
        Извлечение списка товаров из ответа API.
        
        Args:
            response: Response объект
            
        Returns:
            Список товаров
        """
        if response is None:
            return []
            
        try:
            data = response.json()
            if isinstance(data, dict):
                if 'products' in data:
                    return data['products']
                if 'data' in data:
                    if isinstance(data['data'], dict) and 'products' in data['data']:
                        return data['data']['products']
                    if isinstance(data['data'], list):
                        return data['data']
            return []
        except (ValueError, AttributeError):
            return []
    
    def get_products_count(self, response: Optional[Response]) -> int:
        """
        Получение количества найденных товаров.
        
        Args:
            response: Response объект
            
        Returns:
            Количество товаров
        """
        products = self.get_products_from_response(response)
        return len(products)