from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from utils import get_user_name
from keyboards import get_main_menu

# Создаем роутер для команд
commands_router = Router()


@commands_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды /start
    """
    user_name = get_user_name(message)
    await message.answer(
        f"🎓 <b>Добро пожаловать в School Bot!</b>\n\n"
        f"Привет, <b>{user_name}!</b> 👋\n\n"
        f"Я помогу тебе с школьными делами. Используй меню ниже для навигации или просто пиши сообщения - я понимаю ключевые слова!\n\n"
        f"<i>💡 Выбери нужный раздел в меню:</i>",
        reply_markup=get_main_menu()
    )


@commands_router.message(Command("menu"))
async def command_menu_handler(message: Message) -> None:
    """
    Обработчик команды /menu - показывает главное меню
    """
    user_name = get_user_name(message)
    await message.answer(
        f"🎓 <b>Главное меню School Bot</b>\n\n"
        f"Привет, {user_name}! 👋\n"
        f"Выберите нужный раздел:",
        reply_markup=get_main_menu()
    )


@commands_router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    Обработчик команды /help
    """
    help_text = (
        "📚 <b>Справка по School Bot</b>\n\n"
        "🤖 <b>Основные команды:</b>\n"
        "• /start - начать работу с ботом\n"
        "• /menu - показать главное меню\n"
        "• /help - эта справка\n"
        "• /info - информация о боте\n\n"
        "💬 <b>Как общаться:</b>\n"
        "Просто пишите сообщения! Бот понимает:\n"
        "• Приветствия (привет, hello)\n"
        "• Прощания (пока, bye)\n"
        "• Благодарности (спасибо, thanks)\n"
        "• Школьные темы (школа, учёба)\n\n"
        "📱 <b>Интерактивное меню:</b>\n"
        "Используйте кнопки для быстрой навигации!"
    )
    from keyboards import get_back_button
    await message.answer(help_text, reply_markup=get_back_button())


@commands_router.message(Command("info"))
async def command_info_handler(message: Message) -> None:
    """
    Обработчик команды /info
    """
    info_text = (
        "ℹ️ <b>Информация о School Bot</b>\n\n"
        "🤖 <b>Название:</b> School Bot Helper\n"
        "📦 <b>Версия:</b> 1.1.0\n"
        "👨‍💻 <b>Разработчик:</b> @Vprog2\n"
        "🔧 <b>Технологии:</b> Python + aiogram 3.0\n"
        "📅 <b>Дата релиза:</b> 17.10.2025\n\n"
        "🎯 <b>Цель:</b>\n"
        "Помочь школьникам организовать учебный процесс и быть в курсе всех школьных дел.\n\n"
        "🆕 <b>Что нового в версии 1.1.0:</b>\n"
        "• Интерактивное меню с кнопками\n"
        "• Улучшенная навигация\n"
        "• Расширенная справочная система\n"
        "• Более удобный интерфейс\n\n"
        "💡 <b>Идеи и предложения:</b>\n"
        "Свяжитесь с разработчиком для улучшения бота!"
    )
    from keyboards import get_back_button
    await message.answer(info_text, reply_markup=get_back_button())


def register_commands(dp):
    """
    Регистрация роутера команд в диспетчере
    """
    dp.include_router(commands_router)