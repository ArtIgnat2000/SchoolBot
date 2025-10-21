# 🔧 Решение проблемы с правами Docker на Synology

## ❌ Ошибка
```
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock
```

## 🎯 Быстрые решения

### Решение 1: Запуск через sudo (Рекомендуемый для Synology)
```bash
# Вместо обычного запуска
bash deploy-synology.sh

# Используйте sudo (работает всегда)
sudo bash deploy-synology.sh
```

### Решение 2: Изменение прав на Docker socket (Простое)
```bash
# Временно (до перезагрузки) изменить права на Docker socket
sudo chmod 666 /var/run/docker.sock

# После этого можно запускать без sudo
bash deploy-synology.sh
```

### Решение 3: Добавление в группу docker (если доступно)
```bash
# Попробуйте разные команды (одна из них может сработать):

# Стандартная команда (может не работать на Synology)
sudo usermod -aG docker $USER

# Альтернативная команда
sudo adduser $USER docker

# Специфичная для Synology (если доступна)
sudo synogroup --add docker $USER

# ВАЖНО: Перелогиниться для применения изменений
exit
ssh admin@your_synology_ip
```

### Решение 4: Через Container Manager GUI (Надежное)
1. Откройте **Container Manager** в DSM
2. Перейдите в **Project** → **Create**
3. Укажите папку с проектом: `/volume1/docker/school-bot/`
4. Выберите файл: `docker-compose.synology.yml`
5. Нажмите **Build** и затем **Start**

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

### Ограничения DSM (DiskStation Manager)
- Команда `usermod` может быть недоступна в некоторых версиях DSM
- Права на Docker управляются через Container Manager
- Не все стандартные Linux команды доступны

### Synology-специфичные команды
```bash
# Проверка доступных команд управления группами
command -v usermod    # Может отсутствовать
command -v adduser    # Альтернатива
command -v synogroup  # Специфично для Synology

# Попробуйте по очереди:
sudo adduser $USER docker
sudo synogroup --add docker $USER
```

### Рекомендуемый подход для Synology:

#### Вариант A: Всегда использовать sudo
```bash
# Самый надежный способ
sudo bash deploy-synology.sh
sudo docker ps
sudo docker logs school-bot
```

#### Вариант B: Изменить права на socket
```bash
# Однократно выполнить (после каждой перезагрузки)
sudo chmod 666 /var/run/docker.sock

# Затем работать без sudo
bash deploy-synology.sh
docker ps
```

#### Вариант C: Использовать Container Manager GUI
1. **Package Center** → **Container Manager** 
2. **Project** → **Create**
3. Указать путь: `/volume1/docker/school-bot/`
4. Выбрать: `docker-compose.synology.yml`
5. **Build** → **Start**

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