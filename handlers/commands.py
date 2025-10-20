import json
from aiogram import Router, F
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


# Обработчик данных из Mini App (web_app_data)
@commands_router.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    """
    Безопасный обработчик данных из Web App
    """
    # Проверяем, что web_app_data существует и не None
    if not message.web_app_data or not message.web_app_data.data:
        await message.answer("❌ Не получены данные из Web App. Попробуйте снова.")
        return
    
    try:
        data_str = message.web_app_data.data  # Безопасно получаем JSON-строку
        web_data = json.loads(data_str)
        
        # Обрабатываем данные в зависимости от типа
        if 'schedule' in web_data:
            # Данные расписания
            await handle_schedule_data(message, web_data)
        elif 'order' in web_data:
            # Данные заказа (если будет использоваться)
            await handle_order_data(message, web_data)
        else:
            # Общие данные
            user_name = get_user_name(message)
            await message.answer(
                f"✅ <b>Данные получены из Web App!</b>\n\n"
                f"Пользователь: {user_name}\n"
                f"Данные: {json.dumps(web_data, ensure_ascii=False, indent=2)}"
            )
            
    except json.JSONDecodeError as e:
        await message.answer(f"❌ Ошибка в формате данных: {str(e)}")
    except Exception as e:
        await message.answer(f"❌ Произошла ошибка при обработке: {str(e)}")


async def handle_schedule_data(message: Message, data: dict):
    """Обработчик данных расписания из Web App"""
    user_name = get_user_name(message)
    schedule_info = data.get('schedule', {})
    
    selected_day = schedule_info.get('day', 'неизвестно')
    selected_class = schedule_info.get('class', '3В')
    
    response_text = (
        f"📅 <b>Выбрано в Web App</b>\n\n"
        f"👤 Пользователь: {user_name}\n"
        f"📚 Класс: {selected_class}\n"
        f"📆 День: {selected_day}\n\n"
        f"💡 <i>Данные успешно получены из веб-расписания!</i>"
    )
    
    from keyboards import get_back_button
    await message.answer(response_text, reply_markup=get_back_button())


async def handle_order_data(message: Message, data: dict):
    """Обработчик данных заказа из Web App (для будущего использования)"""
    order = data.get('order', {})
    customer = order.get('customer', 'Неизвестен')
    total = order.get('total', 0)
    items = order.get('items', [])
    
    await message.answer(
        f"✅ <b>Заказ получен!</b>\n\n"
        f"👤 Заказчик: {customer}\n"
        f"💰 Сумма: {total} руб.\n"
        f"📦 Товары: {', '.join(items) if items else 'Не указано'}"
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
        "📦 <b>Версия:</b> 1.2.0\n"
        "👨‍💻 <b>Разработчик:</b> @Vprog2\n"
        "🔧 <b>Технологии:</b> Python + aiogram 3.0\n"
        "📅 <b>Дата релиза:</b> 20.10.2025\n\n"
        "🎯 <b>Цель:</b>\n"
        "Помочь школьникам организовать учебный процесс и быть в курсе всех школьных дел.\n\n"
        "🆕 <b>Что нового в версии 1.2.0:</b>\n"
        "• 🌐 Интеграция с веб-расписанием\n"
        "• 📱 Поддержка Telegram Web Apps\n"
        "• 🔗 Внешние ссылки на сайты\n"
        "• 📋 Текстовое расписание в чате\n"
        "• 🛡️ Улучшенная безопасность обработки данных\n\n"
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