from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Filter
from utils import get_user_name, safe_text_check

# Создаем роутер для сообщений
messages_router = Router()


class TextMessageFilter(Filter):
    """
    Фильтр для текстовых сообщений
    """
    async def __call__(self, message: Message) -> bool:
        return message.text is not None and not message.text.startswith('/')


@messages_router.message(TextMessageFilter())
async def text_message_handler(message: Message) -> None:
    """
    Обработчик текстовых сообщений
    """
    user_text = message.text
    user_name = get_user_name(message)
    
    # Проверяем, что текст сообщения не None
    if not user_text:
        await message.answer("🤔 Получено пустое сообщение!")
        return
    
    # Простые ответы на ключевые слова
    if safe_text_check(user_text, ['привет', 'здравствуй', 'hello', 'hi']):
        await message.answer(
            f"Привет, {user_name}! 👋\n"
            f"Как дела в школе?"
        )
    elif safe_text_check(user_text, ['пока', 'до свидания', 'bye']):
        await message.answer(
            f"До свидания, {user_name}! 👋\n"
            f"Удачи в учёбе!"
        )
    elif safe_text_check(user_text, ['спасибо', 'благодарю', 'thanks']):
        await message.answer(
            f"Пожалуйста, {user_name}! 😊\n"
            f"Всегда рад помочь!"
        )
    elif safe_text_check(user_text, ['школа', 'учёба', 'урок']):
        await message.answer(
            f"📚 Отлично! Расскажи больше о своих школьных делах.\n"
            f"Какой предмет изучаешь?"
        )
    else:
        # Эхо-ответ для всех остальных сообщений
        await message.answer(
            f"Ты написал: <i>{user_text}</i>\n\n"
            f"Попробуй написать команду /help для получения справки!"
        )


@messages_router.message()
async def other_message_handler(message: Message) -> None:
    """
    Обработчик всех остальных типов сообщений (фото, видео, стикеры и т.д.)
    """
    if message.photo:
        await message.answer("📸 Красивое фото! К сожалению, я пока не умею их анализировать.")
    elif message.video:
        await message.answer("🎥 Интересное видео! Жаль, что я не могу его посмотреть.")
    elif message.document:
        await message.answer("📄 Документ получен! Пока я не умею их обрабатывать.")
    elif message.sticker:
        await message.answer("😄 Классный стикер! Я тоже люблю стикеры!")
    elif message.voice:
        await message.answer("🎤 Голосовое сообщение! К сожалению, я пока не умею их слушать.")
    else:
        await message.answer("🤔 Интересный тип сообщения! Попробуй отправить текст или команду.")


def register_messages(dp):
    """
    Регистрация роутера сообщений в диспетчере
    """
    dp.include_router(messages_router)