from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from keyboards import (
    get_main_menu, get_help_menu, get_school_menu, 
    get_settings_menu, get_back_button
)
from utils import get_user_name
import logging

# Создаем роутер для callback'ов
callbacks_router = Router()

# Настройка логгера
logger = logging.getLogger(__name__)


async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup=None):
    """
    Безопасное редактирование сообщения с проверкой типов
    """
    try:
        # Проверяем, что message существует и это действительно Message (не InaccessibleMessage)
        if callback.message and isinstance(callback.message, Message):
            await callback.message.edit_text(text=text, reply_markup=reply_markup)
        elif callback.message and hasattr(callback.message, 'answer'):
            # Если не можем отредактировать, отправляем новое сообщение
            await callback.message.answer(text=text, reply_markup=reply_markup)
        elif callback.bot and callback.from_user:
            # Последняя попытка через бота
            await callback.bot.send_message(
                chat_id=callback.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    except (TelegramBadRequest, AttributeError) as e:
        logger.warning(f"Не удалось отредактировать сообщение: {e}")
        # В случае ошибки пытаемся отправить новое сообщение
        try:
            if callback.bot and callback.from_user:
                await callback.bot.send_message(
                    chat_id=callback.from_user.id,
                    text=text,
                    reply_markup=reply_markup
                )
        except Exception as inner_e:
            logger.error(f"Критическая ошибка отправки сообщения: {inner_e}")


@callbacks_router.callback_query(lambda c: c.data == "menu")
async def show_main_menu(callback: CallbackQuery):
    """
    Показывает главное меню
    """
    try:
        user_name = get_user_name(callback)
    except:
        user_name = "Пользователь"
    
    menu_text = (
        f"🎓 <b>Главное меню School Bot</b>\n\n"
        f"Привет, {user_name}! 👋\n"
        f"Выберите нужный раздел:"
    )
    
    await safe_edit_message(callback, menu_text, get_main_menu())
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data == "help")
async def show_help_menu(callback: CallbackQuery):
    """
    Показывает меню справки
    """
    help_text = (
        "📚 <b>Справка по боту</b>\n\n"
        "Выберите раздел справки:"
    )
    
    await safe_edit_message(callback, help_text, get_help_menu())
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data == "help_commands")
async def show_help_commands(callback: CallbackQuery):
    """
    Показывает справку по командам
    """
    commands_text = (
        "🤖 <b>Команды бота:</b>\n\n"
        "🏠 <code>/start</code> - начать работу с ботом\n"
        "🔄 <code>/menu</code> - показать главное меню\n\n"
        "<b>Через кнопки меню:</b>\n"
        "📚 Справка - подробная помощь\n"
        "ℹ️ О боте - информация о боте\n"
        "🎓 Школьные дела - учебные функции\n"
        "⚙️ Настройки - персонализация\n\n"
        "<i>Также можно просто писать сообщения - бот понимает ключевые слова!</i>"
    )
    
    await callback.message.edit_text(
        text=commands_text,
        reply_markup=get_back_button()
    )
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data == "help_chat")
async def show_help_chat(callback: CallbackQuery):
    """
    Показывает справку по общению
    """
    chat_text = (
        "💬 <b>Как общаться с ботом:</b>\n\n"
        "<b>Бот понимает:</b>\n"
        "👋 Приветствия: привет, hello, hi\n"
        "👋 Прощания: пока, bye, до свидания\n"
        "🙏 Благодарности: спасибо, thanks\n"
        "🎓 Школьные темы: школа, учёба, урок\n\n"
        "<b>Типы сообщений:</b>\n"
        "📝 Текстовые сообщения\n"
        "📷 Фотографии\n"
        "🎥 Видео\n"
        "📄 Документы\n"
        "😄 Стикеры\n"
        "🎤 Голосовые сообщения\n\n"
        "<i>Просто пишите естественно - бот вас поймет!</i>"
    )
    
    await callback.message.edit_text(
        text=chat_text,
        reply_markup=get_back_button()
    )
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data == "help_features")
async def show_help_features(callback: CallbackQuery):
    """
    Показывает справку по возможностям
    """
    features_text = (
        "📋 <b>Возможности бота:</b>\n\n"
        "🎓 <b>Школьные функции:</b>\n"
        "• Расписание уроков (в разработке)\n"
        "• Домашние задания (в разработке)\n"
        "• Оценки и успеваемость (в разработке)\n"
        "• Информация о предметах (в разработке)\n\n"
        "🤖 <b>Интеллектуальные ответы:</b>\n"
        "• Распознавание ключевых слов\n"
        "• Контекстные ответы\n"
        "• Поддержка разных типов медиа\n\n"
        "⚙️ <b>Настройки:</b>\n"
        "• Персонализация интерфейса\n"
        "• Уведомления\n"
        "• Языковые настройки\n\n"
        "<i>Больше функций появится в следующих версиях!</i>"
    )
    
    await callback.message.edit_text(
        text=features_text,
        reply_markup=get_back_button()
    )
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data == "info")
async def show_info(callback: CallbackQuery):
    """
    Показывает информацию о боте
    """
    info_text = (
        "ℹ️ <b>Информация о боте:</b>\n\n"
        "🤖 <b>Название:</b> School Bot Helper\n"
        "📦 <b>Версия:</b> 1.1.0\n"
        "👨‍💻 <b>Разработчик:</b> School Bot Team\n"
        "🔧 <b>Технологии:</b> Python + aiogram 3.0\n"
        "📅 <b>Дата релиза:</b> 17.10.2025\n\n"
        "🎯 <b>Цель:</b>\n"
        "Помочь школьникам организовать учебный процесс и быть в курсе всех школьных дел.\n\n"
        "🆕 <b>Что нового в версии 1.1.0:</b>\n"
        "• Интерактивное меню с кнопками\n"
        "• Улучшенная навигация\n"
        "• Расширенная справочная система\n\n"
        "💡 <b>Идеи и предложения:</b>\n"
        "Напишите разработчикам для улучшения бота!"
    )
    
    await callback.message.edit_text(
        text=info_text,
        reply_markup=get_back_button()
    )
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data == "school")
async def show_school_menu(callback: CallbackQuery):
    """
    Показывает меню школьных функций
    """
    school_text = (
        "🎓 <b>Школьные дела</b>\n\n"
        "Выберите нужный раздел:\n\n"
        "<i>💡 Многие функции находятся в разработке и будут доступны в следующих версиях!</i>"
    )
    
    await callback.message.edit_text(
        text=school_text,
        reply_markup=get_school_menu()
    )
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data in ["schedule", "homework", "grades", "subjects"])
async def show_school_feature(callback: CallbackQuery):
    """
    Показывает конкретную школьную функцию
    """
    feature_map = {
        "schedule": {
            "title": "📅 Расписание",
            "text": "Здесь будет отображаться расписание уроков на сегодня и на неделю."
        },
        "homework": {
            "title": "📝 Домашние задания", 
            "text": "Здесь можно будет просматривать и добавлять домашние задания по предметам."
        },
        "grades": {
            "title": "📊 Оценки",
            "text": "Здесь будут отображаться ваши оценки и статистика успеваемости."
        },
        "subjects": {
            "title": "📖 Предметы",
            "text": "Здесь будет информация о всех изучаемых предметах и учителях."
        }
    }
    
    feature = feature_map.get(callback.data)
    if feature:
        feature_text = (
            f"{feature['title']}\n\n"
            f"{feature['text']}\n\n"
            f"🚧 <b>В разработке</b>\n"
            f"Эта функция будет доступна в следующих версиях бота.\n\n"
            f"🎯 <b>Планируемые возможности:</b>\n"
            f"• Просмотр и редактирование\n"
            f"• Уведомления и напоминания\n"
            f"• Интеграция с учебными системами\n"
            f"• Статистика и аналитика"
        )
        
        await callback.message.edit_text(
            text=feature_text,
            reply_markup=get_back_button()
        )
    
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data == "settings")
async def show_settings_menu(callback: CallbackQuery):
    """
    Показывает меню настроек
    """
    settings_text = (
        "⚙️ <b>Настройки</b>\n\n"
        "Персонализируйте работу бота под себя:"
    )
    
    await callback.message.edit_text(
        text=settings_text,
        reply_markup=get_settings_menu()
    )
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data.startswith("settings_"))
async def show_settings_feature(callback: CallbackQuery):
    """
    Показывает конкретную настройку
    """
    settings_map = {
        "settings_notifications": {
            "title": "🔔 Уведомления",
            "text": "Настройка push-уведомлений о домашних заданиях, расписании и оценках."
        },
        "settings_language": {
            "title": "🌐 Язык интерфейса",
            "text": "Выбор языка интерфейса бота (русский, английский)."
        },
        "settings_theme": {
            "title": "🎨 Тема оформления",
            "text": "Настройка внешнего вида сообщений и эмодзи."
        }
    }
    
    setting = settings_map.get(callback.data)
    if setting:
        setting_text = (
            f"{setting['title']}\n\n"
            f"{setting['text']}\n\n"
            f"🚧 <b>В разработке</b>\n"
            f"Эта настройка будет доступна в следующих версиях бота.\n\n"
            f"💡 <b>Пока что бот работает с настройками по умолчанию.</b>"
        )
        
        await callback.message.edit_text(
            text=setting_text,
            reply_markup=get_back_button()
        )
    
    await callback.answer()


def register_callbacks(dp):
    """
    Регистрация роутера callback'ов в диспетчере
    """
    dp.include_router(callbacks_router)