from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards import get_main_menu, get_back_button
from utils import get_user_name

# Создаем роутер для callback'ов
callbacks_router = Router()


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
            await callback.message.edit_text(text=menu_text, reply_markup=get_main_menu())
            
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
            await callback.message.edit_text(text=info_text, reply_markup=get_back_button())
            
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
            await callback.message.edit_text(text=help_text, reply_markup=get_back_button())
            
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
            await callback.message.edit_text(text=feature_text, reply_markup=get_back_button())
            
        else:
            # Для всех неизвестных callback'ов возвращаем в меню
            await callback.answer("Функция в разработке")
            user_name = get_user_name(callback)
            menu_text = (
                f"🎓 <b>Главное меню School Bot</b>\n\n"
                f"Привет, {user_name}! 👋\n"
                f"Выберите нужный раздел:"
            )
            await callback.message.edit_text(text=menu_text, reply_markup=get_main_menu())
            
    except Exception as e:
        # В случае ошибки просто отвечаем на callback
        await callback.answer(f"Произошла ошибка: {str(e)}")
    
    # Всегда отвечаем на callback
    await callback.answer()


def register_callbacks(dp):
    """Регистрация роутера callback'ов в диспетчере"""
    dp.include_router(callbacks_router)