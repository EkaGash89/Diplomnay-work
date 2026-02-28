import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ChitaiGorodAPI:
    """Клиент для работы с API Читай-город"""
    
    def __init__(self, api_key=None):
        self.base_url = os.getenv('BASE_URL', 'https://www.chitai-gorod.ru')
        self.api_key = api_key or os.getenv('API_KEY')
        self.timeout = int(os.getenv('TIMEOUT', 30))
    
    def get_headers(self, include_auth=True):
        """Получение стандартных заголовков для запросов"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if include_auth and self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    def get_search_params(self, phrase, page=1, per_page=60):
        """Получение стандартных параметров поиска"""
        return {
            "customerCityId": "213",
            "products[page]": str(page),
            "products[per-page]": str(per_page),
            "phrase": phrase,
            "abTestGroup": "1"
        }
    
    def extract_product_title(self, product):
        """Извлечение названия книги из продукта с учетом разных структур ответа"""
        if "attributes" in product:
            return product["attributes"].get("title", "")
        elif "title" in product:
            return product.get("title", "")
        return ""
    
    def search_product(self, phrase, page=1, per_page=60):
        """Поиск товаров по фразе"""
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
    
    def search_without_auth(self, phrase):
        """Выполнение поиска без авторизации (для тестов)"""
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
    
    def get_products_from_response(self, response):
        """Извлечение списка товаров из ответа API"""
        if response is None:
            return []
            
        try:
            data = response.json()
            # Пробуем разные пути к товарам в структуре ответа
            if isinstance(data, dict):
                if 'products' in data:
                    return data['products']
                elif 'data' in data and 'products' in data['data']:
                    return data['data']['products']
                elif isinstance(data.get('data'), list):
                    return data['data']
            return []
        except:
            return []
    
    def get_products_count(self, response):
        """Получение количества найденных товаров"""
        products = self.get_products_from_response(response)
        return len(products)