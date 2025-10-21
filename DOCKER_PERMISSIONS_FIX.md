# 🔧 Решение проблемы с правами Docker на Synology

## ❌ Ошибка
```
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock
```

## 🎯 Быстрые решения

### Решение 1: Запуск через sudo (Рекомендуемый)
```bash
# Вместо обычного запуска
bash deploy-synology.sh

# Используйте sudo
sudo bash deploy-synology.sh
```

### Решение 2: Добавление в группу docker (Постоянное решение)
```bash
# Добавить текущего пользователя в группу docker
sudo usermod -aG docker $USER

# Или для конкретного пользователя
sudo usermod -aG docker admin

# ВАЖНО: Перелогиниться для применения изменений
exit
# Затем подключиться заново через SSH
ssh admin@your_synology_ip
```

### Решение 3: Временное изменение прав
```bash
# Временно (до перезагрузки) изменить права на Docker socket
sudo chmod 666 /var/run/docker.sock

# После этого можно запускать без sudo
bash deploy-synology.sh
```

## 🤖 Автоматическое исправление

Обновленный скрипт `deploy-synology.sh` теперь автоматически:

1. **Проверяет права доступа** к Docker
2. **Предлагает решения** при обнаружении проблемы
3. **Может автоматически исправить** права доступа

### Пример автоматического исправления:
```bash
bash deploy-synology.sh
# Скрипт обнаружит проблему и предложит варианты:
# 1. Запустить через sudo
# 2. Добавить в группу docker
# 3. Изменить права временно
```

## 🔍 Проверка текущих прав

```bash
# Проверить, в каких группах состоит пользователь
groups $USER

# Должна быть группа "docker"
# Если нет - добавить через usermod

# Проверить доступ к Docker
docker info
# Если работает без sudo - права в порядке
```

## 🏠 Особенности Synology

### Container Manager и права
- Container Manager устанавливает Docker с ограниченными правами
- По умолчанию только `root` может обращаться к Docker daemon
- Администраторы NAS не всегда автоматически добавляются в группу `docker`

### Безопасное решение для Synology:
```bash
# 1. Добавить admin в группу docker
sudo usermod -aG docker admin

# 2. Перезагрузить Container Manager (если нужно)
sudo systemctl restart docker

# 3. Перелогиниться
exit
ssh admin@your_synology_ip

# 4. Проверить доступ
docker ps
```

## 🚀 Готовые команды для копирования

### Полное исправление прав:
```bash
# Выполнить все команды по порядку:

# 1. Добавить в группу docker
sudo usermod -aG docker $USER

# 2. Изменить права на socket (временно)
sudo chmod 666 /var/run/docker.sock

# 3. Проверить доступ
docker info

# 4. Запустить бота
bash deploy-synology.sh
```

### Если ничего не помогает:
```bash
# Использовать sudo для всех Docker команд
sudo bash deploy-synology.sh
sudo docker ps
sudo docker logs school-bot
sudo docker-compose -f docker-compose.synology.yml down
```

## ✅ Проверка решения

После применения любого из решений:

```bash
# Должно работать без ошибок:
docker info
docker ps
docker-compose version

# Если всё в порядке - запускаем бота:
bash deploy-synology.sh
```

## 🔄 Альтернативные методы

### Через Container Manager GUI:
1. Откройте Container Manager
2. Перейдите в Project 
3. Создайте новый проект с docker-compose.synology.yml
4. Запустите через интерфейс

### Через Portainer (если установлен):
1. Откройте Portainer веб-интерфейс
2. Перейдите в Stacks
3. Создайте новый stack с содержимым docker-compose.synology.yml
4. Deploy stack

## 📞 Если проблема остается

1. **Проверьте Container Manager**:
   - Package Center → Container Manager → убедитесь что запущен

2. **Перезапустите Docker**:
   ```bash
   sudo systemctl restart docker
   ```

3. **Проверьте логи Docker**:
   ```bash
   sudo journalctl -u docker
   ```

4. **Используйте sudo во всех случаях**:
   ```bash
   sudo bash deploy-synology.sh
   ```

---

**💡 Рекомендация**: Для Synology NAS лучше всего использовать `sudo bash deploy-synology.sh` - это самый надежный способ избежать проблем с правами.