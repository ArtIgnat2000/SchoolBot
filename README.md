# 🎓 School Bot - Telegram Bot для школьников

Современный Telegram бот для управления школьными делами с поддержкой интерактивного меню, веб-интеграции и развертывания на Synology NAS.

## ✨ Возможности

- 🎯 **Интерактивное меню** с inline кнопками
- 🌐 **Веб-интеграция** с расписанием (Web Apps + внешние ссылки)
- 📱 **Telegram Web Apps** для встроенного просмотра
- 🔗 **Внешние ссылки** для открытия в браузере
- 📋 **Текстовое расписание** прямо в чате
- 🐳 **Docker поддержка** с оптимизацией для Synology NAS
- 🛡️ **Безопасная обработка** всех типов сообщений
- 📊 **Модульная архитектура** для легкого расширения

## 🚀 Быстрый старт

### Локальная разработка

#### 1. Создание виртуального окружения

**Windows (PowerShell):**
```powershell
# Перейти в папку проекта
cd "d:\TG_Bots\School_Bot"

# Создать виртуальное окружение
python -m venv venv

# Активировать окружение
.\venv\Scripts\Activate.ps1

# Если возникает ошибка с политикой выполнения:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows (Command Prompt):**
```cmd
cd "d:\TG_Bots\School_Bot"
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
cd /path/to/School_Bot
python3 -m venv venv
source venv/bin/activate
```

#### 2. Установка зависимостей
```bash
# Обновить pip
python -m pip install --upgrade pip

# Установить зависимости
pip install -r requirements.txt
```

#### 3. Настройка бота
```bash
# Создать .env файл
cp .env.example .env

# Отредактировать .env файл:
# BOT_TOKEN=your_bot_token_here
# ADMIN_ID=your_admin_id_here
```

#### 4. Запуск
```bash
python main.py
```

### 🏠 Развертывание на Synology NAS

School Bot полностью поддерживает развертывание на Synology NAS через Container Manager.

#### Быстрый старт
```bash
# 1. Загрузите проект на NAS в /volume1/docker/school-bot/
# 2. Подключитесь по SSH
ssh admin@your_synology_ip
cd /volume1/docker/school-bot/

# 3. Запустите интерактивную настройку
bash setup-synology.sh

# 4. Разверните бота
bash deploy-synology.sh
```

#### Альтернативно через Container Manager
1. Package Center → Container Manager
2. Image → Build → указать путь к проекту
3. Container → Create → настроить переменные окружения
4. Запустить контейнер

📖 **Подробное руководство**: [SYNOLOGY_DEPLOYMENT.md](SYNOLOGY_DEPLOYMENT.md)  
⚡ **Быстрый старт**: [QUICK_START_SYNOLOGY.md](QUICK_START_SYNOLOGY.md)

### 🐳 Docker развертывание

#### Локальный Docker
```bash
# Сборка и запуск
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

#### Оптимизированная сборка
```bash
# Использование оптимизированного Dockerfile
docker build -f Dockerfile.optimized -t school-bot:optimized .
docker run -d --name school-bot --env-file .env school-bot:optimized
```

## 📋 Конфигурация

## Проверка установки

```bash
# Проверить установленные пакеты
pip list

# Проверить версию Python
python --version

# Проверить aiogram
python -c "import aiogram; print(aiogram.__version__)"
```

## Деактивация окружения

### Переменные окружения (.env)
```env
# Обязательные
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id_here

# Опциональные
PYTHONUNBUFFERED=1
TZ=Europe/Moscow

# Для продвинутых функций
DB_HOST=localhost
REDIS_URL=redis://localhost:6379
```

## 🌐 Веб-интеграция

School Bot поддерживает интеграцию с веб-сайтом расписания:

- **🌐 Внешние ссылки** - открытие в браузере
- **📱 Telegram Web Apps** - встроенный просмотр в Telegram  
- **📋 Текстовое расписание** - быстрый просмотр в чате

📖 **Документация**: [WEB_INTEGRATION.md](WEB_INTEGRATION.md)

## 📚 Документация

| Файл | Описание |
|------|----------|
| [SYNOLOGY_DEPLOYMENT.md](SYNOLOGY_DEPLOYMENT.md) | Полное руководство по развертыванию на Synology NAS |
| [QUICK_START_SYNOLOGY.md](QUICK_START_SYNOLOGY.md) | Быстрый старт для Synology |
| [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | Работа с Docker, решение проблем |
| [WEB_INTEGRATION.md](WEB_INTEGRATION.md) | Веб-интеграция и Web Apps |
| [WEB_APP_TESTING.md](WEB_APP_TESTING.md) | Тестирование Web App функций |
| [CHANGELOG.md](CHANGELOG.md) | История версий и изменений |

## 🛠️ Разработка

### Структура проекта
```
School_Bot/
├── main.py                 # Точка входа
├── config.py              # Конфигурация
├── keyboards.py           # Inline клавиатуры
├── utils.py              # Вспомогательные функции
├── handlers/             # Обработчики событий
│   ├── commands.py       # Команды (/start, /help)
│   ├── messages.py       # Текстовые сообщения
│   └── callbacks_fixed.py # Callback обработчики
├── requirements.txt      # Зависимости Python
├── Dockerfile           # Docker образ
├── docker-compose*.yml  # Docker Compose конфигурации
└── docs/               # Документация
```

### Команды разработки
```bash
# Запуск в режиме разработки
python main.py

# Проверка кода
python -m py_compile main.py

# Тестирование импортов
python -c "import main; print('OK')"

# Docker сборка
docker build -t school-bot .

# Docker Compose
docker-compose up -d --build
```

## 🚀 Версии

- **v1.2.0** - Веб-интеграция, Synology поддержка
- **v1.1.1** - Исправления безопасности aiogram 3.0
- **v1.1.0** - Интерактивное меню
- **v1.0.0** - Базовая функциональность

## 📞 Поддержка

- **Разработчик**: @Vprog2
- **GitHub Issues**: Сообщения о багах и предложения
- **Документация**: Полные руководства в папке проекта

## 📄 Лицензия

Проект распространяется под MIT лицензией. См. LICENSE файл для деталей.

---

**🎓 School Bot** - помогаем школьникам организовать учебный процесс! 📚

# Очистить кэш
pip cache purge
```