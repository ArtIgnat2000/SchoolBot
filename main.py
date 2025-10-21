import asyncio
import logging
import signal
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

# Импорт конфигурации и обработчиков
from config import config
from handlers import register_commands, register_messages, register_callbacks

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создание объектов бота и диспетчера
bot = Bot(
    token=config.BOT_TOKEN or '',
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


async def main() -> None:
    """
    Главная функция для запуска бота
    """
    # Регистрируем обработчики
    register_commands(dp)
    register_messages(dp)
    register_callbacks(dp)
    
    logger.info("🔄 Бот запускается в РЕЖИМЕ РАЗРАБОТКИ...")
    logger.info("📁 Код загружается с хоста (внешний код)")
    
    try:
        # Удаляем webhook и запускаем polling
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Запускаем бота
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки (Ctrl+C)")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
    finally:
        logger.info("Бот остановлен")
        await bot.session.close()


if __name__ == "__main__":
    try:
        # Запуск бота
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Программа остановлена пользователем")
        sys.exit(0)
