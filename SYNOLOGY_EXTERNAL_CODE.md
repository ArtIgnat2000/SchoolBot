# 🔄 Внешний код на Synology NAS

## Обзор

Теперь School Bot поддерживает **2 режима разработки** на Synology NAS, которые позволяют редактировать код прямо на NAS без пересборки Docker образа.

## 🚀 Быстрый старт

### 1. Развертывание с внешним кодом

```bash
# На Synology NAS через SSH
cd /volume1/docker/school-bot
./deploy-synology.sh

# Выберите один из режимов разработки:
# 4) Режим разработки с авто-reload
# 5) Внешний код без авто-reload
```

### 2. Редактирование кода

```bash
# Код находится в папке развертывания
/volume1/docker/school-bot/

# Основные файлы для редактирования:
├── main.py              # Точка входа
├── config.py            # Конфигурация
├── utils.py             # Утилиты
├── keyboards.py         # Клавиатуры
├── handlers/            # Обработчики
│   ├── commands.py
│   ├── messages.py
│   └── callbacks_fixed.py
└── .env                 # Настройки бота
```

## 🔧 Режимы работы

### 📦 Продакшн режимы (код в образе)
- `docker-compose.yml` - Базовый
- `docker-compose.synology.yml` - Оптимизированный
- `docker-compose.synology-compatible.yml` - Совместимый

### 💻 Режимы разработки (внешний код)
- `docker-compose.dev.yml` - **Авто-reload** ⚡
- `docker-compose.external-code.yml` - Простое монтирование

## ⚡ Режим с авто-reload (Рекомендуемый)

**Файл:** `docker-compose.dev.yml`

### Особенности:
- ✅ Автоматический перезапуск при изменениях
- ✅ Весь проект монтируется с хоста
- ✅ Мгновенное применение изменений
- ✅ Watchdog отслеживает изменения файлов

### Использование:
```bash
# Развертывание
./deploy-synology.sh
# Выберите: 4) Режим разработки с авто-reload

# Редактирование через File Station
# 1. Откройте File Station
# 2. Перейдите в /docker/school-bot/
# 3. Отредактируйте любой .py файл
# 4. Сохраните - бот перезапустится автоматически!

# Просмотр логов
docker logs school-bot-dev -f
```

## 📁 Простое монтирование

**Файл:** `docker-compose.external-code.yml`

### Особенности:
- ✅ Простота настройки
- ✅ Конкретные файлы монтируются
- ⚡ Ручной перезапуск после изменений
- ✅ Больший контроль

### Использование:
```bash
# Развертывание
./deploy-synology.sh
# Выберите: 5) Внешний код без авто-reload

# Редактирование
# 1. Измените файлы в /docker/school-bot/
# 2. Перезапустите контейнер:
docker-compose -f docker-compose.external-code.yml restart

# Просмотр логов
docker logs school-bot-external-code -f
```

## 🛠️ Практические примеры

### Добавление новой команды

1. **Отредактируйте** `handlers/commands.py`:
```python
@router.message(Command("hello"))
async def hello_command(message: Message):
    await message.answer("👋 Привет из внешнего кода!")
```

2. **В режиме авто-reload** - изменения применятся мгновенно
3. **В простом режиме** - перезапустите контейнер

### Изменение клавиатуры

1. **Отредактируйте** `keyboards.py`:
```python
def get_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🆕 Новая кнопка", callback_data="new_button")
    # ... остальные кнопки
    return keyboard.as_markup()
```

2. **Сохраните файл** - изменения видны сразу

### Обновление конфигурации

1. **Отредактируйте** `.env`:
```env
# Добавьте новые настройки
NEW_FEATURE_ENABLED=true
DEBUG_MODE=false
```

2. **Перезапустите контейнер** (в любом режиме):
```bash
docker-compose -f docker-compose.dev.yml restart
```

## 📋 Управление контейнерами

### Основные команды

```bash
# Просмотр статуса
docker ps

# Логи (авто-reload)
docker logs school-bot-dev -f

# Логи (простой режим)
docker logs school-bot-external-code -f

# Перезапуск
docker-compose -f docker-compose.dev.yml restart
docker-compose -f docker-compose.external-code.yml restart

# Остановка
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.external-code.yml down

# Переключение на продакшн
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.synology.yml up -d
```

### Отладка

```bash
# Подключение к контейнеру
docker exec -it school-bot-dev bash

# Просмотр монтированных файлов
docker exec -it school-bot-dev ls -la /app/

# Проверка watchdog (только в авто-reload)
docker exec -it school-bot-dev ps aux | grep watchmedo
```

## 🔄 Переключение между режимами

### Из продакшн в разработку
```bash
# Остановить продакшн
docker-compose -f docker-compose.synology.yml down

# Запустить разработку
docker-compose -f docker-compose.dev.yml up -d
```

### Из разработки в продакшн
```bash
# Остановить разработку
docker-compose -f docker-compose.dev.yml down

# Пересобрать образ с новым кодом
docker-compose -f docker-compose.synology.yml build --no-cache

# Запустить продакшн
docker-compose -f docker-compose.synology.yml up -d
```

## 🎯 Рекомендации

### Для активной разработки:
- Используйте **авто-reload** режим
- Редактируйте код через File Station или SSH
- Следите за логами для отладки

### Для тестирования:
- Используйте **простое монтирование**
- Контролируйте перезапуски вручную
- Тестируйте изменения пошагово

### Для продакшн:
- Переключитесь на продакшн режим
- Код будет встроен в образ
- Максимальная стабильность

## 🚨 Важные замечания

### Безопасность
- Внешний код доступен для редактирования
- Будьте осторожны с правами доступа
- Регулярно делайте резервные копии

### Производительность
- Режимы разработки могут быть медленнее
- Для продакшн используйте встроенный код
- Watchdog потребляет дополнительные ресурсы

### Обновления
- Изменения в `requirements.txt` требуют пересборки
- Dockerfile изменения требуют пересборки
- Python код обновляется мгновенно

## 📞 Поддержка

При возникновении проблем:

1. **Проверьте логи:**
   ```bash
   docker logs school-bot-dev -f
   ```

2. **Проверьте монтирование:**
   ```bash
   docker inspect school-bot-dev | grep Mounts -A 10
   ```

3. **Перезапустите контейнер:**
   ```bash
   docker-compose -f docker-compose.dev.yml restart
   ```

4. **Обратитесь к основной документации:**
   - `EXTERNAL_CODE_GUIDE.md`
   - `SYNOLOGY_DEPLOYMENT.md`