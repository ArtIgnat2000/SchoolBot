# 🔧 Решение ошибки CPU CFS scheduler на Synology

## ❌ Ошибка
```
Error response from daemon: NanoCPUs can not be set, as your kernel does not support CPU CFS scheduler or the cgroup is not mounted
```

## 🎯 Причина
Synology NAS не поддерживает ограничения CPU через Docker Compose или cgroup настроен неправильно.

## ✅ Быстрые решения

### Решение 1: Использовать совместимую конфигурацию
```bash
# Запустить с совместимой конфигурацией (без CPU ограничений)
docker-compose -f docker-compose.synology-compatible.yml up -d
```

### Решение 2: Через обновленный скрипт
```bash
# Обновленный deploy-synology.sh автоматически обнаружит проблему
bash deploy-synology.sh
# Выберите опцию 3) Совместимая с старыми Synology
```

### Решение 3: Ручное редактирование
Отредактируйте `docker-compose.synology.yml`:
```yaml
# Закомментируйте или удалите секцию CPU ограничений
deploy:
  resources:
    limits:
      memory: 256M
      # cpus: '0.5'  # Отключить эту строку
    reservations:
      memory: 128M
      # cpus: '0.25'  # Отключить эту строку
```

### Решение 4: Запуск без deploy секции
```bash
# Создайте упрощенную версию docker-compose.yml
# Удалите полностью секцию deploy:
```

## 🔄 Автоматическое исправление

Обновленный `deploy-synology.sh` теперь:
1. **Пытается запустить** с обычной конфигурацией
2. **Обнаруживает ошибку** CFS scheduler
3. **Автоматически переключается** на совместимую версию
4. **Продолжает работу** без ограничений CPU

## 📋 Доступные конфигурации

| Файл | Описание | CPU ограничения |
|------|----------|-----------------|
| `docker-compose.yml` | Базовая | Нет |
| `docker-compose.synology.yml` | Оптимизированная | Есть (могут не работать) |
| `docker-compose.synology-compatible.yml` | Совместимая | Отключены |

## 🚀 Рекомендуемые команды

### Для старых Synology NAS:
```bash
# Использовать совместимую конфигурацию
docker-compose -f docker-compose.synology-compatible.yml up -d --build

# Проверить статус
docker ps

# Просмотр логов
docker logs school-bot -f
```

### Для новых Synology NAS:
```bash
# Попробовать обычную конфигурацию
docker-compose -f docker-compose.synology.yml up -d

# Если ошибка - переключиться на совместимую
docker-compose -f docker-compose.synology-compatible.yml up -d
```

## 🔍 Диагностика

### Проверка поддержки CFS scheduler:
```bash
# Проверить наличие cgroup
mount | grep cgroup

# Проверить CPU controller
cat /proc/cgroups | grep cpu

# Информация о ядре
uname -a
```

### Проверка Docker возможностей:
```bash
# Информация о Docker
docker info | grep -i cpu

# Версия Docker Compose
docker-compose --version
```

## 💡 Альтернативные ограничения

Если нужно ограничить ресурсы, используйте Docker run параметры:
```bash
# Запуск с ограничениями через docker run
docker run -d \
  --name school-bot \
  --memory=256m \
  --restart=unless-stopped \
  --env-file .env \
  school-bot:latest
```

## ⚠️ Примечания

- **CPU ограничения** не критичны для Telegram бота
- **Память ограничения** обычно работают нормально
- **Бот будет работать** без CPU ограничений
- **Performance** останется приемлемым для NAS

## ✅ Проверка решения

После применения любого решения:
```bash
# Должно работать без ошибок
docker ps
docker logs school-bot --tail 20

# Бот должен отвечать в Telegram
# Отправьте /start боту для проверки
```

---

**💡 Рекомендация**: Для Synology NAS лучше использовать `docker-compose.synology-compatible.yml` - это избавит от проблем с CFS scheduler и обеспечит стабильную работу.