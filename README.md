# API и UI тесты для интернет-магазина "Читай-город"

## Описание проекта
Проект содержит автоматизированные UI и API тесты для интернет-магазина "Читай-город".

### UI тесты
Проверка функциональности сайта:
- Авторизация (валидация поля ввода телефона)
- Добавление книг в корзину
- Изменение количества товаров
- Подсчет суммы товаров
- Фильтрация и сортировка в разделе распродажа
- Очистка корзины

### API тесты
Тестирование поискового сервиса API

## Структура файлов
├── tests/
│ ├── init.py
│ ├── test_api.py # API тесты
│ ├── test_ui.py # UI тесты
│ ├── conftest.py # Фикстуры pytest
│ ├── ui_test_data.py # Константы и тестовые данные
│ └── ui_helpers.py # Вспомогательные функции
├── api_client.py # API клиент
├── .env # Переменные окружения
├── .env.example # Пример переменных окружения
├── requirements.txt # Зависимости
├── pytest.ini # Конфигурация pytest
└── README.md # Документация

## Предварительные требования
- Python 3.8+
- Установленные зависимости из requirements.txt
- Браузер Chrome (для UI тестов)
- Действующий API ключ (обновляется каждый час)

## Быстрый старт

### 1. Клонирование репозитория

git clone <repository-url>
cd <project-directory>
### 2. Создание виртуального окружения (рекомендуется)

Windows
python -m venv venv
venv\Scripts\activate

Linux/Mac
python3 -m venv venv
source venv/bin/activate
### 3. Установка зависимостей

pip install -r requirements.txt

### 4. Настройка переменных окружения
cp .env.example .env

# Отредактируйте .env файл, указав актуальные данные

### Переменные окружения
Основные переменные (.env)

#API Configuration
API_KEY=your_api_key_here           # Действует 1 час
BASE_URL=https://web-agr.chitai-gorod.ru/web/api/v2
TIMEOUT=30                          # Таймаут запросов

#UI Configuration
TEST_PHONE=your_phone_here          # Телефон для авторизации
TEST_PASSWORD=your_password_here    # Пароль для авторизации

#Environment
ENVIRONMENT=testing                  # Окружение

Важно!
API_KEY обновляется каждый час. Перед запуском API тестов необходимо получить актуальный ключ

### Режимы запуска тестов

# Все тесты
pytest

# Все тесты с подробным выводом
pytest -v

## Только API тесты
pytest test/test_api.py -v

## Только UI тесты
pytest test/test_ui.py -v

## API + UI тесты вместе
pytest test/test_api.py tests/test_ui.py -v

# По маркерам
Маркеры тестов:
positive - Позитивные тесты
negative - Негативные тесты
ui - UI тесты
api - API тесты
smoke - Smoke тесты (критический функционал)
regression - Регрессионные тесты

# API тесты по маркерам
pytest test/test_api.py -m positive -v
pytest test/test_api.py -m negative -v
pytest test/test_api.py -m smoke -v

# UI тесты по маркерам
pytest test/test_ui.py -m positive -v
pytest test/test_ui.py -m negative -v
pytest test/test_ui.py -m smoke -v

# Конкретный тест
pytest test/test_api.py::TestSearchAPI::test_search_by_cyrillic_title -v

# Конкретный тест-класс
pytest test/test_ui.py::TestAuthorization -v

# Конкретный тест
pytest test/test_ui.py::TestAuthorization::test_phone_validation_complete -v
pytest test/test_ui.py::TestCart::test_add_book_to_cart -v
pytest test/test_ui.py::TestFilters::test_sales_filters -v
pytest test/test_ui.py::TestCompleteScenarios::test_complete_shopping_flow -v
pytest test/test_ui.py::TestCartQuantityAndSum::test_quantity_and_sum -v
pytest test/test_ui.py::TestCartClear::test_add_and_clear -v



# По Severity (Allure)

## Запуск с разными уровнями важности
pytest --alluredir=allure-results

# Режимы отладки

## С выводом print в консоль
pytest -v -s

## Остановка при первой ошибке
pytest -x

## Запуск только упавших тестов
pytest --lf

## Запуск тестов по порядку (без перемешивания)
pytest -p no:randomly

## Повторный запуск упавших тестов
pytest --last-failed

## Поиск и фильтрация тестов: По имени теста
pytest -k "search" -v
pytest -k "test_search_by_cyrillic" -v

## Поиск и фильтрация тестов: По имени файла
pytest test/test_api.py::TestSearchAPI -v

## Поиск и фильтрация тестов: Конкретный тест
pytest test/test_api.py::TestSearchAPI::test_search_by_cyrillic_title -v

## Исключение тестов
pytest -k "not slow" -v

# Отчеты

# Установка Allure (если не установлен)
## Windows (через scoop)
scoop install allure
## Mac
brew install allure
## Linux
sudo apt-get install allure

# Запуск тестов с сохранением результатов
pytest --alluredir=allure-results

# Генерация и открытие отчета
allure serve allure-results

# Генерация отчета без открытия
allure generate allure-results -o allure-report --clean

# Открытие существующего отчета
allure open allure-report

# Структура тестов
UI тесты (test_ui.py)
TestAuthorization - Тесты авторизации
test_phone_input_validation - Проверка валидации поля телефона
TestCart - Тесты корзины
test_add_book_to_cart - Добавления книги в корзину и проверки счетчика
TestFilters - Тесты фильтрации и сортировки
test_sales_filters - Фильтры в разделе распродажа
TestCartQuantityAndSum - Тест на изменение количества товара и пересчет суммы
test_quantity_and_sum - проверка пересчета суммы
TestCartClear - Тест на добавление двух товаров и полная очистка корзины
test_add_two_and_clear - полная очистка корзины

API тесты (test_api.py)
TestSearchAPI - Тесты поискового API
Поиск по кириллице
Поиск с цифрами
Поиск с латиницей
Негативные сценарии
Граничные случаи

# Тестовые данные
API тесты используют следующие категории запросов:
Кириллица: "мертвые души", "война и мир", "преступление и наказание", "мастер и маргарита"
С цифрами: "1984", "451 градус", "100 лет", "50 оттенков"
Латиница: "harry potter", "lord of the rings", "game of thrones", "dune", "python"
Спецсимволы: "!@#$%", "***", "___", "{}[]", "\/", "~`
Различная длина: от 1 до 1000 символов

# Дополнительная информация

Финальный проект по ручному тестированию:
https://katygashtest.yonote.ru/share/2656fa9a-74a3-4c44-b77b-d3552247b47a#h-funkcional%D1%8Cnoe-testirovanie

Логин: eka4717@mail.ru
Пароль: Yonote53590!