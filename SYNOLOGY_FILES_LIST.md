# Создание архива для загрузки на Synology NAS

## Файлы для включения в архив

### Обязательные файлы проекта
main.py
config.py  
keyboards.py
utils.py
requirements.txt
Dockerfile

### Папка handlers
handlers/__init__.py
handlers/commands.py
handlers/messages.py
handlers/callbacks_fixed.py

### Файлы для Synology
docker-compose.synology.yml
setup-synology.sh
deploy-synology.sh

### Конфигурационные файлы
.dockerignore
.gitignore

### Дополнительные Docker файлы
Dockerfile.optimized
docker-compose.yml

### Документация
README.md
SYNOLOGY_DEPLOYMENT.md
QUICK_START_SYNOLOGY.md
DOCKER_GUIDE.md
WEB_INTEGRATION.md

## Команды для создания архива

### Windows (PowerShell)
```powershell
# Создание ZIP архива с нужными файлами
Compress-Archive -Path main.py,config.py,keyboards.py,utils.py,requirements.txt,Dockerfile,handlers,docker-compose.synology.yml,setup-synology.sh,deploy-synology.sh,.dockerignore,README.md,SYNOLOGY_DEPLOYMENT.md,QUICK_START_SYNOLOGY.md -DestinationPath school-bot-synology.zip
```

### Linux/macOS
```bash
# Создание tar.gz архива
tar -czf school-bot-synology.tar.gz \
  main.py config.py keyboards.py utils.py requirements.txt \
  Dockerfile handlers/ docker-compose.synology.yml \
  setup-synology.sh deploy-synology.sh .dockerignore \
  README.md SYNOLOGY_DEPLOYMENT.md QUICK_START_SYNOLOGY.md
```

### Ручной отбор файлов
1. Создайте папку `school-bot-for-synology`
2. Скопируйте туда файлы из списка выше
3. Заархивируйте папку

## После загрузки на NAS

1. Распакуйте архив в `/volume1/docker/school-bot/`
2. Установите права доступа:
   ```bash
   chmod +x setup-synology.sh deploy-synology.sh
   ```
3. Запустите настройку:
   ```bash
   bash setup-synology.sh
   ```