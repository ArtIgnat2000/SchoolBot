from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from keyboards import get_main_menu, get_back_button
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
        if callback.message and hasattr(callback.message, 'edit_text'):
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
    
    feature_name = feature_names.get(callback.data, "Функция")
    
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


@callbacks_router.callback_query()
async def handle_unknown_callback(callback: CallbackQuery):
    """Обработка неизвестных callback'ов"""
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