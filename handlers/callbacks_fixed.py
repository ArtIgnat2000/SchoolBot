from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from keyboards import (
    get_main_menu, get_back_button, get_web_schedule_options,
    get_mini_app_keyboard, get_external_link_keyboard
)
from utils import get_user_name
import logging

# Создаем роутер для callback'ов
callbacks_router = Router()

# Настройка логгера
logger = logging.getLogger(__name__)


async def safe_answer_callback(callback: CallbackQuery, text: str = "", show_alert: bool = False):
    """Безопасный ответ на callback с обработкой ошибок"""
    try:
        await callback.answer(text=text, show_alert=show_alert)
    except Exception as e:
        logger.warning(f"Не удалось ответить на callback: {e}")


async def safe_edit_or_send(callback: CallbackQuery, text: str, reply_markup=None):
    """
    Безопасное редактирование или отправка сообщения
    """
    try:
        # Пытаемся отредактировать существующее сообщение
        if callback.message and isinstance(callback.message, Message) and hasattr(callback.message, 'edit_text'):
            await callback.message.edit_text(text=text, reply_markup=reply_markup)
            return True
    except (TelegramBadRequest, AttributeError) as e:
        logger.info(f"Не удалось отредактировать сообщение, отправляем новое: {e}")
    
    # Если редактирование не удалось, отправляем новое сообщение
    try:
        if callback.message and hasattr(callback.message, 'answer'):
            await callback.message.answer(text=text, reply_markup=reply_markup)
            return True
    except Exception as e:
        logger.warning(f"Не удалось отправить через message.answer: {e}")
    
    # Последняя попытка - через бота
    try:
        if callback.bot and callback.from_user:
            await callback.bot.send_message(
                chat_id=callback.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
            return True
    except Exception as e:
        logger.error(f"Критическая ошибка отправки сообщения: {e}")
        return False


@callbacks_router.callback_query(lambda c: c.data == "menu")
async def show_main_menu(callback: CallbackQuery):
    """Показать главное меню"""
    user_name = get_user_name(callback)
    menu_text = (
        f"🎓 <b>Главное меню School Bot</b>\n\n"
        f"Привет, {user_name}! 👋\n"
        f"Выберите нужный раздел:"
    )
    
    await safe_edit_or_send(callback, menu_text, get_main_menu())
    await safe_answer_callback(callback)


@callbacks_router.callback_query(lambda c: c.data == "info")
async def show_info(callback: CallbackQuery):
    """Показать информацию о боте"""
    info_text = (
        "ℹ️ <b>Информация о School Bot</b>\n\n"
        "🤖 <b>Название:</b> School Bot Helper\n"
        "📦 <b>Версия:</b> 1.1.0\n"
        "👨‍💻 <b>Разработчик:</b> @Vprog2\n"
        "🔧 <b>Технологии:</b> Python + aiogram 3.0\n"
        "📅 <b>Дата релиза:</b> 17.10.2025\n\n"
        "🎯 <b>Цель:</b> Помочь школьникам организовать учебный процесс\n\n"
        "🆕 <b>Новое в версии 1.1.0:</b>\n"
        "• Интерактивное меню с кнопками\n"
        "• Улучшенная навигация\n"
        "• Расширенная справочная система"
    )
    
    await safe_edit_or_send(callback, info_text, get_back_button())
    await safe_answer_callback(callback)


@callbacks_router.callback_query(lambda c: c.data == "help")
async def show_help(callback: CallbackQuery):
    """Показать справку"""
    help_text = (
        "📚 <b>Справка по School Bot</b>\n\n"
        "🤖 <b>Команды:</b>\n"
        "• /start - начать работу\n"
        "• /menu - главное меню\n"
        "• /help - справка\n"
        "• /info - информация\n\n"
        "💬 <b>Общение:</b>\n"
        "Пишите сообщения - бот понимает ключевые слова!\n\n"
        "📱 <b>Навигация:</b>\n"
        "Используйте кнопки для удобства"
    )
    
    await safe_edit_or_send(callback, help_text, get_back_button())
    await safe_answer_callback(callback)


@callbacks_router.callback_query(lambda c: c.data in ["school", "settings"])
async def show_feature_in_development(callback: CallbackQuery):
    """Показать функцию в разработке"""
    feature_names = {
        "school": "🎓 Школьные дела",
        "settings": "⚙️ Настройки"
    }
    
    # Безопасное получение названия функции с дополнительной проверкой
    feature_name = feature_names.get(callback.data if callback.data else "", "Неизвестная функция")
    
    if callback.data == "school":
        # Для школьных дел показываем полное меню
        from keyboards import get_school_menu
        school_text = (
            f"🎓 <b>Школьные дела</b>\n\n"
            f"Выберите нужный раздел:\n\n"
            f"📅 <b>Расписание</b> - просмотр уроков\n"
            f"📝 <b>Домашние задания</b> - учет заданий\n"
            f"📊 <b>Оценки</b> - успеваемость\n"
            f"📖 <b>Предметы</b> - информация о предметах\n"
            f"🌐 <b>Веб-расписание</b> - интерактивное расписание\n\n"
            f"<i>💡 Некоторые функции находятся в разработке</i>"
        )
        await safe_edit_or_send(callback, school_text, get_school_menu())
    else:
        # Для настроек показываем "в разработке"
        feature_text = (
            f"🚧 <b>{feature_name}</b>\n\n"
            f"Эта функция находится в разработке и будет доступна в следующих версиях бота.\n\n"
            f"🎯 <b>Планируемые возможности:</b>\n"
            f"• Расписание уроков\n"
            f"• Домашние задания\n"
            f"• Оценки и успеваемость\n"
            f"• Настройки уведомлений\n"
            f"• Персонализация интерфейса\n\n"
            f"💡 <b>Следите за обновлениями!</b>"
        )
        await safe_edit_or_send(callback, feature_text, get_back_button())
    
    await safe_answer_callback(callback)


@callbacks_router.callback_query(lambda c: c.data == "web_schedule")
async def show_web_schedule_options(callback: CallbackQuery):
    """Показать варианты доступа к веб-расписанию"""
    web_text = (
        "🌐 <b>Веб-расписание</b>\n\n"
        "Выберите способ просмотра интерактивного расписания:\n\n"
        "🌐 <b>В браузере</b> - откроется в отдельной вкладке\n"
        "📱 <b>Web App</b> - откроется внутри Telegram\n"
        "📋 <b>Текстом</b> - покажет расписание в чате\n\n"
        "💡 <i>Web App позволяет использовать расписание не выходя из Telegram!</i>"
    )
    
    await safe_edit_or_send(callback, web_text, get_web_schedule_options())
    await safe_answer_callback(callback)


@callbacks_router.callback_query(lambda c: c.data == "show_schedule_text")
async def show_schedule_text(callback: CallbackQuery):
    """Показать расписание в текстовом виде"""
    schedule_text = (
        "📅 <b>Расписание 3 «В» класса</b>\n\n"
        "<b>📚 ПОНЕДЕЛЬНИК:</b>\n"
        "1️⃣ 8:30-9:10 - <i>Пустой урок</i>\n"
        "2️⃣ 9:30-10:10 - 📊 Математика\n"
        "3️⃣ 10:20-11:00 - 📝 Русский язык\n"
        "4️⃣ 11:20-12:00 - 🌍 Иностранный язык (английский)\n"
        "5️⃣ 12:20-13:00 - 🌍 Иностранный язык (английский)\n"
        "6️⃣ 13:10-13:50 - 📚 Литературное чтение\n\n"
        "🏠 <b>Навигация:</b>\n"
        "🍽️ ЕДА | 🏃 КАНИКУЛЫ | 📍 ДОП\n\n"
        "📊 <b>Система оценок:</b>\n"
        "🔴 40-69 - Удовлетворительно\n"
        "🟡 70-84 - Хорошо\n"
        "🟢 85-100 - Отлично\n\n"
        "💡 <i>Для полного интерактивного расписания используйте веб-версию!</i>"
    )
    
    await safe_edit_or_send(callback, schedule_text, get_external_link_keyboard())
    await safe_answer_callback(callback)


@callbacks_router.callback_query(lambda c: c.data == "schedule_info")
async def show_schedule_info(callback: CallbackQuery):
    """Показать информацию о расписании"""
    info_text = (
        "ℹ️ <b>О веб-расписании</b>\n\n"
        "🎯 <b>Возможности:</b>\n"
        "• 📅 Просмотр расписания по дням недели\n"
        "• 🎨 Цветовая индикация предметов\n"
        "• 📊 Система оценок с цветовыми кодами\n"
        "• 🔄 Быстрая навигация по неделям\n"
        "• 📱 Адаптивный дизайн для всех устройств\n\n"
        "🔧 <b>Технологии:</b>\n"
        "• HTML5 + CSS3 + JavaScript\n"
        "• Адаптивная верстка\n"
        "• Интеграция с Telegram Bot API\n\n"
        "🚀 <b>Как использовать:</b>\n"
        "1. Нажмите кнопку открытия расписания\n"
        "2. Выберите день недели\n"
        "3. Просматривайте уроки и время\n"
        "4. Используйте навигационные кнопки\n\n"
        "💡 <i>Рекомендуем использовать Web App для лучшего опыта!</i>"
    )
    
    await safe_edit_or_send(callback, info_text, get_mini_app_keyboard())
    await safe_answer_callback(callback)


@callbacks_router.callback_query()
async def handle_unknown_callback(callback: CallbackQuery):
    """Обработка неизвестных callback'ов"""
    callback_data = getattr(callback, 'data', 'unknown')
    logger.info(f"Получен неизвестный callback: {callback_data}")
    await safe_answer_callback(callback, "🔄 Функция в разработке", show_alert=True)
    
    # Возвращаем в главное меню
    user_name = get_user_name(callback)
    menu_text = (
        f"🎓 <b>Главное меню School Bot</b>\n\n"
        f"Привет, {user_name}! 👋\n"
        f"Выберите нужный раздел:"
    )
    
    await safe_edit_or_send(callback, menu_text, get_main_menu())


def register_callbacks(dp):
    """Регистрация роутера callback'ов в диспетчере"""
    dp.include_router(callbacks_router)