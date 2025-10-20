from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


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
                    text="🌐 Открыть веб-расписание",
                    callback_data="web_schedule"
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


def get_web_schedule_options() -> InlineKeyboardMarkup:
    """
    Создает меню вариантов доступа к веб-расписанию
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌐 Открыть в браузере",
                    url="https://artignat2000.github.io/Sedule3B/index.htm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📱 Web App (в Telegram)",
                    web_app=WebAppInfo(url="https://artignat2000.github.io/Sedule3B/index.htm")
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Показать расписание здесь",
                    callback_data="show_schedule_text"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад к школьным делам",
                    callback_data="school"
                )
            ]
        ]
    )
    return keyboard


def get_mini_app_keyboard() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с Mini App кнопкой
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Запустить расписание Mini App",
                    web_app=WebAppInfo(url="https://artignat2000.github.io/Sedule3B/index.htm")
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="school"
                )
            ]
        ]
    )
    return keyboard


def get_external_link_keyboard() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с внешней ссылкой
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌐 Открыть расписание",
                    url="https://artignat2000.github.io/Sedule3B/index.htm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Информация о расписании",
                    callback_data="schedule_info"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="school"
                )
            ]
        ]
    )
    return keyboard