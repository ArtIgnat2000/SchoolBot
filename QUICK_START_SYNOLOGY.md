# 🚀 Быстрый запуск на Synology NAS

## Метод 1: Автоматическая настройка (Рекомендуемый)

### 1. Загрузите файлы на Synology
- Скопируйте все файлы проекта в `/volume1/docker/school-bot/`
- Используйте File Station или SSH

### 2. Подключитесь по SSH
```bash
ssh admin@your_synology_ip
cd /volume1/docker/school-bot/
```

### 3. Запустите интерактивную настройку
```bash
bash setup-synology.sh
```

### 4. Запустите бота
```bash
bash deploy-synology.sh
```

### 5. Проверьте работу
```bash
docker logs school-bot -f
```

---

## Метод 2: Через Container Manager (GUI)

### 1. Откройте Container Manager
- Package Center → Container Manager → Install

### 2. Создайте образ
- Image → Build
- Путь: `/volume1/docker/school-bot/`
- Имя: `school-bot`

### 3. Создайте .env файл
```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id_here
PYTHONUNBUFFERED=1
```

### 4. Запустите контейнер
- Image → school-bot → Launch
- Переменные окружения из .env
- Auto-restart: Always

---

## Метод 3: Одной командой (для опытных)

```bash
# Быстрый запуск с минимальной настройкой
cd /volume1/docker/school-bot/
echo "BOT_TOKEN=YOUR_TOKEN_HERE" > .env
echo "ADMIN_ID=YOUR_ID_HERE" >> .env
docker-compose -f docker-compose.synology.yml up -d --build
```

---

## ⚡ Управление ботом

```bash
# Статус
docker ps

# Логи
docker logs school-bot -f

# Остановка
bash deploy-synology.sh --stop

# Перезапуск  
bash deploy-synology.sh --restart

# Обновление
bash deploy-synology.sh --update
```

---

## 🆘 Troubleshooting

**Проблема**: Контейнер не запускается
```bash
docker logs school-bot  # Проверить ошибки
```

**Проблема**: Не хватает прав
```bash
sudo chmod +x *.sh
sudo chown -R admin:users /volume1/docker/school-bot/
```

**Проблема**: Ошибка сборки образа
```bash
docker system prune -a  # Очистить кэш
docker build --no-cache -t school-bot .  # Пересобрать
```

---

## 📱 Мониторинг

- **Container Manager**: http://your_synology_ip:5000
- **Логи бота**: `docker logs school-bot -f`  
- **Системные ресурсы**: `docker stats school-bot`

---

## 🔄 Автозапуск

**Container Manager**: Auto-restart = Always

**Task Scheduler**: 
- Control Panel → Task Scheduler → Create → User-defined script
- Команда: `bash /volume1/docker/school-bot/start-school-bot.sh`

---

## 📂 Структура файлов

```
/volume1/docker/school-bot/
├── .env                          # Конфигурация (создать)
├── docker-compose.synology.yml   # Docker Compose для Synology  
├── setup-synology.sh            # Интерактивная настройка
├── deploy-synology.sh           # Автодеплой
├── Dockerfile                   # Docker образ
├── main.py                      # Код бота
└── logs/                        # Логи (создается автоматически)
```

**Время развертывания**: 5-10 минут  
**Требования**: 256MB RAM, 1GB диска  
**Поддержка**: Synology DSM 7.0+