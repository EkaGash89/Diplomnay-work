# Diplomnay-work
Для тестирования выбран проект “Читай город”

# API и UI тесты для интернет-магазина "Читай-город"

## Описание проекта
Проект содержит автоматизированные UI тесты для проверки поля "Фамилия" в разделе личных данных на сайте [Читай-город](https://www.chitai-gorod.ru/profile/personal-data). А так же автоматизированные API тесты для поискового сервиса.

Тесты основаны на функциональном чек-листе из финальной работы по ручному тестированию.
ссылка на финальную работ: https://katygashtest.yonote.ru/share/2656fa9a-74a3-4c44-b77b-d3552247b47a

логин: eka4717@mail.ru
пароль: Yonote53590!

## Cтруктура файлов:

├── tests/
│   ├── __init__.py
│   ├── base_test.py              # Базовый класс с общими методами
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_ui.py                 # Главный файл с тестами
│   └── pages/                     # Папка с классами страниц
│       ├── __init__.py
│       ├── login_page.py          # Класс для страницы авторизации
│       └── profile_page.py        # Класс для страницы профиля
├── api_client.py
├── .env
├── requirements.txt
├── pytest.ini
└── README.md

# Инструкция по запуску

перед прогоном тестов необходимо внести данные а файл .env

## Установка зависимостей:
pip install -r requirements.txt

### Запуск всех тестов
pytest test/test_ui.py test/test_api.py

### Запуск только UI-тестов
pytest tests/test_ui.py -v

### Запуск только API-тестов
pytest tests\test_api.py -v

### Запуск с подробным выводом
pytest tests/test_api.py -v -s
pytest tests/test_ui.py -v -s

### Запуск с отчетом Allure
pytest tests/test_api.py --alluredir=allure-results
pytest tests/test_ui.py --alluredir=allure-results

# Запуск всех тестов из обоих файлов с созданием отчета Allure
pytest tests/test_ui.py tests/test_api.py --alluredir=allure-results -v -s

### Открыть отчет Allure
allure serve allure-results

### Запуск конкретного теста
pytest tests/test_api.py::TestSearchAPI::test_search_by_cyrillic_title -v
pytest tests/test_ui.py::TestSurnameField::test_complete_surname_testing -v -s

### Запуск с маркерами
pytest tests/test_api.py -m positive -v

pytest tests/test_ui.py -v -m "positive"
pytest tests/test_ui.py -v -m "negative"


