# 🔄 Руководство по работе с внешним кодом в Docker

## Обзор решений

Для удобной разработки и обновления Python кода без пересборки Docker образа доступно несколько вариантов:

## 🚀 Способ 1: Docker Compose с автоперезапуском (Рекомендуемый для разработки)

### Файл: `docker-compose.dev.yml`

**Особенности:**
- ✅ Полное монтирование кода проекта
- ✅ Автоматический перезапуск при изменениях файлов
- ✅ Исключение кэша Python и виртуального окружения
- ✅ Отключение создания .pyc файлов

**Запуск:**
```bash
# Windows PowerShell
docker-compose -f docker-compose.dev.yml up -d

# Для просмотра логов с автоперезапуском
docker-compose -f docker-compose.dev.yml logs -f
```

**Как работает:**
1. Весь код проекта монтируется в `/app`
2. При изменении любого `.py` файла контейнер автоматически перезапускается
3. Зависимости остаются в контейнере (не нужно переустанавливать)

---

## 📁 Способ 2: Простое монтирование файлов

### Файл: `docker-compose.external-code.yml`

**Особенности:**
- ✅ Простота настройки
- ✅ Монтирование конкретных файлов
- ✅ Ручной перезапуск контейнера для применения изменений
- ✅ Лучший контроль над тем, какие файлы доступны

**Запуск:**
```bash
# Windows PowerShell
docker-compose -f docker-compose.external-code.yml up -d

# Перезапуск после изменений
docker-compose -f docker-compose.external-code.yml restart
```

---

## 🔧 Способ 3: Гибридный подход (Live Reload)

Для продвинутой разработки с мгновенными обновлениями:

**Запуск с live reload:**
```bash
# Сначала запустить контейнер
docker-compose -f docker-compose.dev.yml up -d

# Подключиться к контейнеру для отладки
docker exec -it school-bot-dev bash

# Внутри контейнера можно запустить с nodemon-подобным инструментом
watchmedo auto-restart --directory=/app --pattern='*.py' --recursive -- python main.py
```

---

## 📋 Практические команды

### Управление контейнерами разработки:

```bash
# Запуск в режиме разработки
docker-compose -f docker-compose.dev.yml up -d

# Просмотр логов в реальном времени
docker-compose -f docker-compose.dev.yml logs -f school-bot

# Остановка
docker-compose -f docker-compose.dev.yml down

# Пересборка образа (при изменении Dockerfile.dev)
docker-compose -f docker-compose.dev.yml build --no-cache

# Подключение к контейнеру для отладки
docker exec -it school-bot-dev bash
```

### Переключение между режимами:

```bash
# Остановить продакшн версию
docker-compose down

# Запустить версию для разработки
docker-compose -f docker-compose.dev.yml up -d

# Вернуться к продакшн версии
docker-compose -f docker-compose.dev.yml down
docker-compose up -d
```

---

## 🎯 Рекомендации по использованию

### Для активной разработки:
- Используйте `docker-compose.dev.yml` с автоперезапуском
- Код обновляется мгновенно при сохранении файлов
- Идеально для итеративной разработки

### Для тестирования изменений:
- Используйте `docker-compose.external-code.yml`
- Простой и предсказуемый подход
- Ручной контроль перезапусков

### Для продакшн развертывания:
- Используйте стандартный `docker-compose.yml`
- Код остается внутри образа
- Максимальная стабильность и производительность

---

## 🔍 Структура файлов

```
School_Bot/
├── docker-compose.yml              # Продакшн (код в образе)
├── docker-compose.dev.yml          # Разработка (авто-reload)
├── docker-compose.external-code.yml # Простое монтирование
├── Dockerfile                      # Продакшн образ
├── Dockerfile.dev                  # Образ для разработки
├── main.py                         # ← Ваш код здесь
├── config.py                       # ← Обновляется снаружи
├── handlers/                       # ← Модули обновляются
│   ├── commands.py
│   └── ...
└── .env                           # ← Конфигурация снаружи
```

---

## ⚡ Быстрый старт

1. **Скопируйте код в удобное место:**
   ```bash
   # Весь код уже у вас в d:\TG_Bots\School_Bot\
   ```

2. **Запустите режим разработки:**
   ```bash
   cd d:\TG_Bots\School_Bot\
   docker-compose -f docker-compose.dev.yml up -d
   ```

3. **Редактируйте файлы** в папке `d:\TG_Bots\School_Bot\`

4. **Изменения применяются автоматически!** 🎉

---

## 🐛 Отладка

**Если контейнер не видит изменения:**
```bash
# Проверьте монтирование
docker inspect school-bot-dev | grep -A 10 "Mounts"

# Подключитесь к контейнеру
docker exec -it school-bot-dev bash
ls -la /app/  # Должны быть ваши файлы
```

**Если авто-перезапуск не работает:**
```bash
# Проверьте логи watchdog
docker-compose -f docker-compose.dev.yml logs school-bot

# Ручной перезапуск
docker-compose -f docker-compose.dev.yml restart school-bot
```