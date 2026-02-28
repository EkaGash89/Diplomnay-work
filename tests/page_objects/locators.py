from selenium.webdriver.common.by import By

class PersonalDataPageLocators:
    """Локаторы для страницы личных данных"""
    
    # Поле Фамилия - различные варианты локаторов
    SURNAME_INPUT = (By.CSS_SELECTOR, "input.chg-app-input__control")
    SURNAME_BY_VALUE = (By.CSS_SELECTOR, "input[value='Гашимова']")
    SURNAME_BY_ID = (By.ID, "v-0-65-0")
    SURNAME_BY_PLACEHOLDER = (By.CSS_SELECTOR, "input[placeholder*='фамили']")
    SURNAME_BY_NAME = (By.CSS_SELECTOR, "input[name='surname']")
    SURNAME_BY_TEST = (By.CSS_SELECTOR, "input[data-test='surname-input']")
    
    # Кнопка сохранения
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], button.chg-button, button:contains('Сохранить')")
    
    # Сообщения об успехе/ошибке
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".chg-notification__success, .success-message, [class*='success']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".chg-input__error, .error-message, [class*='error'], .chg-notification__error")
    
    # Поле ввода с ошибкой
    INPUT_WITH_ERROR = (By.CSS_SELECTOR, ".chg-input--error, .error-field")