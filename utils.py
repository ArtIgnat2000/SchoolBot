from aiogram.types import Message, CallbackQuery
from typing import Union


def get_user_name(message_or_callback: Union[Message, CallbackQuery]) -> str:
    """
    Безопасное получение имени пользователя
    
    Args:
        message_or_callback: Объект сообщения или callback от aiogram
        
    Returns:
        str: Имя пользователя или запасной вариант
    """
    # Получаем пользователя из Message или CallbackQuery
    user = None
    if isinstance(message_or_callback, Message):
        user = message_or_callback.from_user
    elif isinstance(message_or_callback, CallbackQuery):
        user = message_or_callback.from_user
    
    if user is None:
        return "Пользователь"
    
    # Используем full_name если доступно, иначе first_name, username или ID
    if user.full_name:
        return user.full_name
    elif user.first_name:
        return user.first_name
    elif user.username:
        return f"@{user.username}"
    else:
        return f"ID{user.id}"


def is_admin(message: Message, admin_ids: list) -> bool:
    """
    Проверяет, является ли пользователь администратором
    
    Args:
        message: Объект сообщения от aiogram
        admin_ids: Список ID администраторов
        
    Returns:
        bool: True если пользователь администратор
    """
    if message.from_user is None:
        return False
    
    return message.from_user.id in admin_ids


def safe_text_check(text: str, keywords: list) -> bool:
    """
    Безопасная проверка текста на наличие ключевых слов
    
    Args:
        text: Текст для проверки
        keywords: Список ключевых слов
        
    Returns:
        bool: True если найдено совпадение
    """
    if not text:
        return False
    
    return any(word in text.lower() for word in keywords)