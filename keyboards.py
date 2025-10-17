from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu() -> InlineKeyboardMarkup:
    """
    Создает главное меню бота с кнопками команд
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📚 Справка",
                    callback_data="help"
                ),
                InlineKeyboardButton(
                    text="ℹ️ О боте",
                    callback_data="info"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎓 Школьные дела",
                    callback_data="school"
                ),
                InlineKeyboardButton(
                    text="⚙️ Настройки",
                    callback_data="settings"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Обновить меню",
                    callback_data="menu"
                )
            ]
        ]
    )
    return keyboard


def get_help_menu() -> InlineKeyboardMarkup:
    """
    Создает меню справки с кнопками разделов
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🤖 Команды бота",
                    callback_data="help_commands"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Как общаться",
                    callback_data="help_chat"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Возможности",
                    callback_data="help_features"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад в меню",
                    callback_data="menu"
                )
            ]
        ]
    )
    return keyboard


def get_school_menu() -> InlineKeyboardMarkup:
    """
    Создает меню школьных функций
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Расписание",
                    callback_data="schedule"
                ),
                InlineKeyboardButton(
                    text="📝 Домашние задания",
                    callback_data="homework"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Оценки",
                    callback_data="grades"
                ),
                InlineKeyboardButton(
                    text="📖 Предметы",
                    callback_data="subjects"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад в меню",
                    callback_data="menu"
                )
            ]
        ]
    )
    return keyboard


def get_settings_menu() -> InlineKeyboardMarkup:
    """
    Создает меню настроек
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔔 Уведомления",
                    callback_data="settings_notifications"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌐 Язык интерфейса",
                    callback_data="settings_language"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎨 Тема оформления",
                    callback_data="settings_theme"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад в меню",
                    callback_data="menu"
                )
            ]
        ]
    )
    return keyboard


def get_back_button() -> InlineKeyboardMarkup:
    """
    Создает простую кнопку "Назад"
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Назад в меню",
                    callback_data="menu"
                )
            ]
        ]
    )
    return keyboard