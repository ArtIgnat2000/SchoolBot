# Развертывание School Bot на Synology NAS

## Предварительные требования

### 1. Установка Docker на Synology
1. Откройте **Package Center** на вашем Synology
2. Найдите и установите **Container Manager** (новая версия) или **Docker** (старая версия)
3. Запустите Container Manager после установки

### 2. Подготовка файлов
Загрузите файлы проекта на Synology через:
- **File Station** (веб-интерфейс)
- **Synology Drive** (синхронизация)
- **SSH/SFTP** (командная строка)

Рекомендуемое расположение: `/volume1/docker/school-bot/`

## Способы развертывания

### Способ 1: Через Container Manager (GUI)

#### Шаг 1: Сборка образа
1. Откройте **Container Manager**
2. Перейдите в **Image** → **Build**
3. Укажите путь к папке с Dockerfile: `/volume1/docker/school-bot/`
4. Название образа: `school-bot`
5. Тег: `latest`
6. Нажмите **Build**

#### Шаг 2: Создание контейнера
1. В разделе **Image** найдите `school-bot:latest`
2. Нажмите **Launch**
3. Настройте контейнер:

**Общие настройки:**
- Container name: `school-bot`
- Execute command: не изменяйте (используется CMD из Dockerfile)
- Auto-restart: ✅ Always

**Переменные окружения:**
```
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id_here
PYTHONUNBUFFERED=1
```

**Ресурсы (опционально):**
- Memory limit: 256 MB
- CPU priority: Normal

4. Нажмите **Next** → **Done**

### Способ 2: Через SSH (Командная строка)

#### Подключение по SSH
```bash
ssh admin@your_synology_ip
sudo -i
```

#### Переход в папку проекта
```bash
cd /volume1/docker/school-bot/
```

#### Сборка образа
```bash
docker build -t school-bot .
```

#### Запуск контейнера
```bash
docker run -d \
  --name school-bot \
  --restart unless-stopped \
  -e BOT_TOKEN="your_bot_token_here" \
  -e ADMIN_ID="your_admin_id_here" \
  -e PYTHONUNBUFFERED=1 \
  school-bot:latest
```

### Способ 3: Docker Compose (Рекомендуемый)

#### Создание .env файла
Создайте файл `.env` в папке `/volume1/docker/school-bot/`:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id_here
PYTHONUNBUFFERED=1
```

#### Запуск через docker-compose
```bash
cd /volume1/docker/school-bot/
docker-compose up -d
```

## Мониторинг и управление

### Через Container Manager
1. **Контейнеры**: Просмотр статуса, запуск/остановка
2. **Логи**: Container Manager → Container → Logs
3. **Терминал**: Container Manager → Container → Terminal
4. **Статистика**: Использование CPU/RAM

### Через SSH
```bash
# Просмотр статуса
docker ps

# Логи
docker logs school-bot -f

# Статистика
docker stats school-bot

# Остановка
docker stop school-bot

# Запуск
docker start school-bot

# Перезапуск
docker restart school-bot
```

## Автозапуск после перезагрузки

### Container Manager
- В настройках контейнера включите **Auto-restart: Always**

### Docker Compose
- Используйте `restart: unless-stopped` в docker-compose.yml

### Systemd (SSH)
Создайте systemd сервис:
```bash
# Создание файла сервиса
cat > /etc/systemd/system/school-bot.service << EOF
[Unit]
Description=School Bot Container
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=true
ExecStart=/usr/local/bin/docker start school-bot
ExecStop=/usr/local/bin/docker stop school-bot

[Install]
WantedBy=multi-user.target
EOF

# Включение автозапуска
systemctl enable school-bot.service
```

## Структура папок на Synology

```
/volume1/docker/school-bot/
├── .env                    # Переменные окружения
├── .dockerignore          # Исключения для Docker
├── Dockerfile             # Основной Dockerfile
├── Dockerfile.optimized   # Оптимизированная версия
├── docker-compose.yml     # Docker Compose конфигурация
├── requirements.txt       # Python зависимости
├── main.py               # Основной файл бота
├── config.py             # Конфигурация
├── keyboards.py          # Клавиатуры
├── utils.py              # Утилиты
├── handlers/             # Обработчики
│   ├── __init__.py
│   ├── commands.py
│   ├── messages.py
│   └── callbacks_fixed.py
└── logs/                 # Логи (создается автоматически)
```

## Безопасность на Synology

### 1. Переменные окружения
- **НЕ храните** токены в открытом виде
- Используйте файл `.env` с правильными правами:
```bash
chmod 600 .env
chown admin:users .env
```

### 2. Сетевая безопасность
- Бот работает только исходящие соединения (к Telegram API)
- Никаких открытых портов не требуется
- Firewall настройки не нужны

### 3. Файловые права
```bash
# Установка правильных прав на проект
chown -R admin:users /volume1/docker/school-bot/
chmod -R 755 /volume1/docker/school-bot/
chmod 600 /volume1/docker/school-bot/.env
```

## Обновление бота

### Автоматическое обновление (рекомендуемый)
1. Остановите контейнер
2. Обновите исходный код
3. Пересоберите образ
4. Запустите контейнер

```bash
cd /volume1/docker/school-bot/

# Остановка
docker-compose down

# Обновление кода (git pull или копирование новых файлов)
git pull origin main

# Пересборка и запуск
docker-compose up -d --build
```

### Ручное обновление через Container Manager
1. Остановите контейнер в Container Manager
2. Удалите старый контейнер (данные в .env сохранятся)
3. Обновите файлы через File Station
4. Пересоберите образ в Container Manager
5. Создайте новый контейнер

## Резервное копирование

### Что резервировать
- Исходный код: `/volume1/docker/school-bot/`
- Конфигурация: `.env`, `docker-compose.yml`
- Логи: `/volume1/docker/school-bot/logs/`

### Автоматическое резервное копирование
Используйте **Hyper Backup** в Synology:
1. Backup & Replication → Hyper Backup
2. Добавьте задачу резервирования
3. Выберите папку `/volume1/docker/school-bot/`
4. Настройте расписание (например, ежедневно)

## Мониторинг и логирование

### Логи через Container Manager
1. Container Manager → Container
2. Выберите `school-bot`
3. Перейдите в **Log**
4. Настройте фильтры по необходимости

### Логи через SSH
```bash
# Последние 100 строк
docker logs school-bot --tail 100

# Следить за логами в реальном времени
docker logs school-bot -f

# Логи с временными метками
docker logs school-bot -t

# Логи за определенный период
docker logs school-bot --since="2025-10-21T00:00:00"
```

### Настройка логирования
В `docker-compose.yml` уже настроено:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## Troubleshooting

### Проблемы сборки
1. **Недостаточно места**: Проверьте свободное место на диске
2. **Сетевые проблемы**: Проверьте интернет-соединение
3. **Права доступа**: Убедитесь что у пользователя есть права на Docker

### Проблемы запуска
1. **Контейнер не запускается**: Проверьте логи `docker logs school-bot`
2. **Переменные окружения**: Убедитесь что BOT_TOKEN корректный
3. **Сетевой доступ**: Проверьте доступ к api.telegram.org

### Полезные команды диагностики
```bash
# Информация о системе
docker system info

# Использование дискового пространства
docker system df

# Диагностика контейнера
docker inspect school-bot

# Процессы в контейнере
docker top school-bot

# Вход в контейнер для отладки
docker exec -it school-bot /bin/bash
```

## Оптимизация производительности

### Ресурсы контейнера
- **RAM**: 128-256 MB достаточно для Telegram бота
- **CPU**: 0.25-0.5 CPU cores
- **Хранилище**: 500 MB для образа + логи

### Настройки Synology
1. **Docker Package**: Убедитесь что выделено достаточно RAM
2. **Storage**: Используйте SSD для Docker директории (если доступно)
3. **Network**: Настройте QoS для стабильного соединения

## Заключение

School Bot успешно работает на Synology NAS с автозапуском, мониторингом и автоматическим резервным копированием. Container Manager предоставляет удобный GUI, а SSH доступ позволяет тонкую настройку через командную строку.

Для production использования рекомендуется:
- ✅ Docker Compose для развертывания
- ✅ Container Manager для мониторинга  
- ✅ Hyper Backup для резервирования
- ✅ Мониторинг логов через web-интерфейс