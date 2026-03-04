"""
Константы и тестовые данные для UI тестов
"""

from selenium.webdriver.common.by import By

# ========== URL'ы ==========
BASE_URL = "https://www.chitai-gorod.ru"
CART_URL = f"{BASE_URL}/cart"
SALES_URL = f"{BASE_URL}/sales"

# ========== Селекторы ==========
class Selectors:
    """Класс с селекторами элементов"""
    
    class Header:
        LOGIN_BUTTON = (By.CSS_SELECTOR, "span.header-controls__text")
        LOGIN_ICON = (By.CSS_SELECTOR, ".header-controls__icon")
        CART_COUNTER = (By.CSS_SELECTOR, "div[data-testid-indicator-header='cartCounter']")
        SEARCH_INPUT = (By.CSS_SELECTOR, "input#app-search")
    
    class Login:
        PHONE_INPUT = (By.CSS_SELECTOR, "input[type='tel']")
        GET_CODE_BUTTON = (By.XPATH, "//button[contains(text(), 'Получить код')]")
    
    class Search:
        BUY_BUTTON = (By.XPATH, "//button[contains(@class, 'product-buttons__main-action') and contains(text(), 'Купить')]")
        FIRST_BUY_BUTTON = (By.XPATH, "(//button[contains(@class, 'product-buttons__main-action') and contains(text(), 'Купить')])[1]")
    
    class Cart:
        CART_ITEM = (By.CSS_SELECTOR, ".cart-item")
        QUANTITY_INPUT = (By.CSS_SELECTOR, ".chg-ui-input-number__input")
        INCREMENT_BUTTON = (By.CSS_SELECTOR, ".chg-ui-input-number__input-control--increment")
        TOTAL_SUM = (By.CSS_SELECTOR, ".info-item__value")
        CLEAR_CART_BUTTON = (By.XPATH, "//div[contains(text(), 'Очистить корзину')]")
        CONFIRM_CLEAR_BUTTON = (By.XPATH, "//button[contains(text(), 'Очистить')]")
        EMPTY_CART_MESSAGE = (By.XPATH, "//div[contains(text(), 'Корзина пуста')]")
        DELETE_BUTTON = (By.CSS_SELECTOR, ".cart-item__delete")
        RESTORE_BUTTON = (By.XPATH, "//div[contains(text(), 'Восстановить корзину')]")
    
    class Filters:
        CATEGORY = (By.XPATH, "//span[contains(text(), 'Художественная литература')]")
        SUBCATEGORY = (By.XPATH, "//span[contains(text(), 'Российская литература')]")
        AUTHOR_INPUT = (By.CSS_SELECTOR, "input[placeholder='Поиск по автору']")
        AUTHOR_SUGGESTION = (By.XPATH, "//span[@class='filter-multiselect-search__dropdown-item' and contains(text(), 'Александр Сергеевич Пушкин')]")
        PRODUCTS_TOTAL = (By.CSS_SELECTOR, ".catalog-products-total")

# ========== Тестовые данные ==========

# Данные для авторизации
PHONE_TEST_CASES = [
    ("(495)123-45-67", True, "Форматированный номер со скобками и дефисами"),
    ("1234567890", True, "Только цифры"),
    ("922 000 12 34", True, "Номер с пробелами"),
    ("495ABC DEFG", True, "С буквами"),
    ("495*12#345", True, "Со спецсимволами"),
    ("-495--123", True, "С дефисами"),
    ("abc", True, "Только буквы"),
    ("!@#$%", True, "Только спецсимволы"),
    ("12", True, "Короткий номер"),
    ("", True, "Пустая строка")
]

# Поисковые запросы
SEARCH_QUERIES = {
    "bulgakov": "Собачье сердце. Булгаков",
    "master": "Мастер и Маргарита",
    "pushkin": "пушкин",
    "griboedov": "Горе от ума. Грибоедов",
    "book1": "Горе от ума. Грибоедов"
}

# Товары для тестирования
PRODUCTS = {
    "viy_id": "3041349",
    "first_product_id": "3080928",
    "second_product_id": "227930",
    "third_product_id": "2994433"
}

PRODUCTS_INFO = {
    "3080928": {"title": "горе от ума грибоедов", "price": 394},
    "227930": {"title": "Преступление и наказание", "price": 296},
    "2994433": {"title": "Война и мир. В 4 томах", "price": 317}
}

# Список тестовых книг
TEST_BOOKS = [
    {"query": "Мастер и Маргарита", "name": "Мастер и Маргарита"},
    {"query": "Собачье сердце. Булгаков", "name": "Собачье сердце"},
    {"query": "Горе от ума. Грибоедов", "name": "Горе от ума"}
]

# Ожидаемые значения
EXPECTED_VALUES = {
    "sales_filter_count": 77,
    "cart_items_after_clear": 0
}

# Тестовые конфигурации
TEST_CONFIG = {
    "cart": {
        "click_count": 3,
        "timeout": 30
    },
    "search": {
        "wait_time": 3
    }
}