import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class Config:
    """
    Класс для хранения конфигурации бота
    """
    # Основные настройки
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # Проверка токена
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден в переменных окружения!")
    
    # ID администраторов
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(","))) if os.getenv("ADMIN_IDS") else []
    
    # Настройки логирования
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Настройки бота
    PARSE_MODE = "HTML"
    
    # Дополнительные настройки
    WEBHOOK_MODE = os.getenv("WEBHOOK_MODE", "False").lower() == "true"
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8000"))


# Создаем экземпляр конфигурации
config = Config()