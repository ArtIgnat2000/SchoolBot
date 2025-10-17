from aiogram import Router
from aiogram.types import CallbackQuery, Message
from keyboards import get_main_menu, get_back_button
from utils import get_user_name

# Создаем роутер для callback'ов
callbacks_router = Router()


async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup=None):
    """
    Безопасное редактирование сообщения с проверкой типов
    """
    try:
        # Проверяем, что message существует и это действительно Message (не InaccessibleMessage)
        if callback.message and isinstance(callback.message, Message):
            await callback.message.edit_text(text=text, reply_markup=reply_markup)
        elif callback.bot and callback.from_user:
            # Если не можем отредактировать, отправляем новое сообщение
            await callback.bot.send_message(
                chat_id=callback.from_user.id,
                text=text,
                reply_markup=reply_markup
            )
    except Exception as e:
        # В случае любой ошибки пытаемся отправить новое сообщение через бота
        try:
            if callback.bot and callback.from_user:
                await callback.bot.send_message(
                    chat_id=callback.from_user.id,
                    text=text,
                    reply_markup=reply_markup
                )
        except Exception as inner_e:
            # Если и это не работает, просто логируем ошибку
            print(f"Критическая ошибка отправки сообщения: {inner_e}, первоначальная ошибка: {e}")


@callbacks_router.callback_query()
async def handle_callbacks(callback: CallbackQuery):
    """Универсальный обработчик всех callback'ов"""
    
    if not callback.data:
        await callback.answer("Ошибка: нет данных")
        return
    
    try:
        if callback.data == "menu":
            user_name = get_user_name(callback)
            menu_text = (
                f"🎓 <b>Главное меню School Bot</b>\n\n"
                f"Привет, {user_name}! 👋\n"
                f"Выберите нужный раздел:"
            )
            await safe_edit_message(callback, menu_text, get_main_menu())
            
        elif callback.data == "info":
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
            await safe_edit_message(callback, info_text, get_back_button())
            
        elif callback.data == "help":
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
            await safe_edit_message(callback, help_text, get_back_button())
            
        elif callback.data in ["school", "settings"]:
            feature_text = (
                "🚧 <b>В разработке</b>\n\n"
                "Эта функция будет доступна в следующих версиях бота.\n\n"
                "🎯 <b>Планируемые возможности:</b>\n"
                "• Расписание уроков\n"
                "• Домашние задания\n"
                "• Оценки и успеваемость\n"
                "• Настройки уведомлений\n\n"
                "💡 Следите за обновлениями!"
            )
            await safe_edit_message(callback, feature_text, get_back_button())
            
        else:
            # Для всех неизвестных callback'ов возвращаем в меню
            await callback.answer("Функция в разработке")
            user_name = get_user_name(callback)
            menu_text = (
                f"🎓 <b>Главное меню School Bot</b>\n\n"
                f"Привет, {user_name}! 👋\n"
                f"Выберите нужный раздел:"
            )
            await safe_edit_message(callback, menu_text, get_main_menu())
            
    except Exception as e:
        # В случае ошибки просто отвечаем на callback
        await callback.answer(f"Произошла ошибка: {str(e)}")
    
    # Всегда отвечаем на callback
    await callback.answer()


def register_callbacks(dp):
    """Регистрация роутера callback'ов в диспетчере"""
    dp.include_router(callbacks_router)