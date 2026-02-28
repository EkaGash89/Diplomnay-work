import pytest
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def api_key():
    """Фикстура для получения API ключа"""
    return os.getenv('API_KEY')