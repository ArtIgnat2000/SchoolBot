# Docker Deployment для School Bot

## Исправление предупреждения JSONArgsRecommended

### Проблема
```
JSONArgsRecommended: JSON arguments recommended for CMD to prevent unintended behavior related to OS signals
```

### Решение
Используйте JSON формат для команды `CMD` вместо shell формата:

❌ **Неправильно:**
```dockerfile
CMD python main.py
```

✅ **Правильно:**
```dockerfile
CMD ["python", "main.py"]
```

## Варианты Dockerfile

### 1. Простой Dockerfile (текущий)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
```

### 2. Оптимизированный Dockerfile
Файл: `Dockerfile.optimized`
- Многоэтапная сборка
- Безопасность (отдельный пользователь)
- Healthcheck
- Меньший размер образа

## Команды для сборки и запуска

### Простая сборка
```bash
# Сборка образа
docker build -t school-bot .

# Запуск контейнера
docker run -d --name school-bot --env-file .env school-bot
```

### С помощью Docker Compose (рекомендуемый)
```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### Оптимизированная сборка
```bash
# Сборка оптимизированного образа
docker build -f Dockerfile.optimized -t school-bot:optimized .

# Запуск с ограничениями ресурсов
docker run -d \
  --name school-bot \
  --memory=256m \
  --cpus=0.5 \
  --restart=unless-stopped \
  --env-file .env \
  school-bot:optimized
```

## Переменные окружения

Создайте файл `.env`:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id_here
PYTHONUNBUFFERED=1
```

## Мониторинг и отладка

### Просмотр логов
```bash
# Docker
docker logs school-bot -f

# Docker Compose
docker-compose logs -f school-bot
```

### Вход в контейнер
```bash
# Docker
docker exec -it school-bot /bin/bash

# Docker Compose
docker-compose exec school-bot /bin/bash
```

### Проверка состояния
```bash
# Статус контейнера
docker ps

# Использование ресурсов
docker stats school-bot

# Healthcheck
docker inspect school-bot | grep Health -A 10
```

## Лучшие практики

### 1. Безопасность
- ✅ Используйте JSON формат для CMD
- ✅ Создавайте отдельного пользователя (не root)
- ✅ Минимизируйте права доступа
- ✅ Используйте .dockerignore

### 2. Оптимизация
- ✅ Многоэтапная сборка (multi-stage)
- ✅ Кэширование слоев
- ✅ Минимальный базовый образ (slim)
- ✅ Очистка кэшей после установки

### 3. Мониторинг
- ✅ Настройка логирования
- ✅ Healthcheck для проверки состояния
- ✅ Ограничения ресурсов
- ✅ Restart policies

## Размеры образов

| Тип Dockerfile | Размер | Особенности |
|----------------|--------|-------------|
| Простой | ~150MB | Быстрая сборка |
| Оптимизированный | ~120MB | Безопасность, здоровье |
| С Alpine | ~80MB | Минимальный размер |

## Производственное развертывание

### Docker Swarm
```bash
# Создание service
docker service create \
  --name school-bot \
  --replicas 1 \
  --env-file .env \
  --restart-condition on-failure \
  school-bot:latest
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: school-bot
spec:
  replicas: 1
  selector:
    matchLabels:
      app: school-bot
  template:
    metadata:
      labels:
        app: school-bot
    spec:
      containers:
      - name: school-bot
        image: school-bot:latest
        env:
        - name: BOT_TOKEN
          valueFrom:
            secretKeyRef:
              name: bot-secrets
              key: token
```

## Troubleshooting

### Частые проблемы

1. **JSONArgsRecommended warning**
   - Решение: Используйте `CMD ["python", "main.py"]`

2. **Большой размер образа**
   - Решение: Используйте multi-stage build

3. **Проблемы с правами**
   - Решение: Создайте пользователя в Dockerfile

4. **Медленная сборка**
   - Решение: Оптимизируйте порядок COPY команд

## Полезные команды

```bash
# Очистка неиспользуемых образов
docker system prune -a

# Анализ слоев образа
docker history school-bot

# Размер образа
docker images school-bot

# Статистика использования
docker stats --no-stream
```