from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from utils import get_user_name

# Создаем роутер для команд
commands_router = Router()


@commands_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды /start
    """
    user_name = get_user_name(message)
    await message.answer(
        f"Привет, <b>{user_name}!</b>\n"
        f"Добро пожаловать в школьного бота!\n\n"
        f"Доступные команды:\n"
        f"/start - начать работу с ботом\n"
        f"/help - показать справку\n"
        f"/info - информация о боте"
    )


@commands_router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    Обработчик команды /help
    """
    help_text = (
        "<b>📚 Справка по командам:</b>\n\n"
        "/start - начать работу с ботом\n"
        "/help - показать эту справку\n"
        "/info - информация о боте\n\n"
        "<i>Отправьте любое сообщение, и бот его повторит!</i>"
    )
    await message.answer(help_text)


@commands_router.message(Command("info"))
async def command_info_handler(message: Message) -> None:
    """
    Обработчик команды /info
    """
    info_text = (
        "<b>🤖 Информация о боте:</b>\n\n"
        "Название: Школьный бот\n"
        "Версия: 1.0.1\n"
        "Разработчик: @Vprog2\n"
        "Построен на: aiogram 3.0\n\n"
        "<i>Этот бот создан для помощи в школьных делах!</i>"
    )
    await message.answer(info_text)


def register_commands(dp):
    """
    Регистрация роутера команд в диспетчере
    """
    dp.include_router(commands_router)