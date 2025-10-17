from aiogram.types import Message


def get_user_name(message: Message) -> str:
    """
    Безопасное получение имени пользователя
    
    Args:
        message: Объект сообщения от aiogram
        
    Returns:
        str: Имя пользователя или запасной вариант
    """
    if message.from_user is None:
        return "Пользователь"
    
    # Используем full_name если доступно, иначе first_name, username или ID
    if message.from_user.full_name:
        return message.from_user.full_name
    elif message.from_user.first_name:
        return message.from_user.first_name
    elif message.from_user.username:
        return f"@{message.from_user.username}"
    else:
        return f"ID{message.from_user.id}"


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