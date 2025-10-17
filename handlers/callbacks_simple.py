from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards import (
    get_main_menu, get_help_menu, get_school_menu, 
    get_settings_menu, get_back_button
)
from utils import get_user_name

# Создаем роутер для callback'ов
callbacks_router = Router()


@callbacks_router.callback_query(lambda c: c.data == "menu")
async def show_main_menu(callback: CallbackQuery):
    """Показывает главное меню"""
    user_name = get_user_name(callback)
    
    menu_text = (
        f"🎓 <b>Главное меню School Bot</b>\n\n"
        f"Привет, {user_name}! 👋\n"
        f"Выберите нужный раздел:"
    )
    
    try:
        await callback.message.edit_text(text=menu_text, reply_markup=get_main_menu())
    except:
        await callback.message.answer(text=menu_text, reply_markup=get_main_menu())
    
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data == "help")
async def show_help_menu(callback: CallbackQuery):
    """Показывает меню справки"""
    help_text = "📚 <b>Справка по боту</b>\n\nВыберите раздел справки:"
    
    try:
        await callback.message.edit_text(text=help_text, reply_markup=get_help_menu())
    except:
        await callback.message.answer(text=help_text, reply_markup=get_help_menu())
    
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data == "help_commands")
async def show_help_commands(callback: CallbackQuery):
    """Показывает справку по командам"""
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
    
    try:
        await callback.message.edit_text(text=commands_text, reply_markup=get_back_button())
    except:
        await callback.message.answer(text=commands_text, reply_markup=get_back_button())
    
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data == "info")
async def show_info(callback: CallbackQuery):
    """Показывает информацию о боте"""
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
    
    try:
        await callback.message.edit_text(text=info_text, reply_markup=get_back_button())
    except:
        await callback.message.answer(text=info_text, reply_markup=get_back_button())
    
    await callback.answer()


@callbacks_router.callback_query(lambda c: c.data == "school")
async def show_school_menu(callback: CallbackQuery):
    """Показывает меню школьных функций"""
    school_text = (
        "🎓 <b>Школьные дела</b>\n\n"
        "Выберите нужный раздел:\n\n"
        "<i>💡 Многие функции находятся в разработке и будут доступны в следующих версиях!</i>"
    )
    
    try:
        await callback.message.edit_text(text=school_text, reply_markup=get_school_menu())
    except:
        await callback.message.answer(text=school_text, reply_markup=get_school_menu())
    
    await callback.answer()


def register_callbacks(dp):
    """Регистрация роутера callback'ов в диспетчере"""
    dp.include_router(callbacks_router)