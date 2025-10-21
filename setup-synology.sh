#!/bin/bash

# Быстрая настройка School Bot для Synology
# Этот скрипт поможет настроить бота в первый раз

echo "🎓 School Bot - Быстрая настройка для Synology"
echo "================================================"
echo ""

# Функции для цветного вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Проверка операционной системы
check_synology() {
    if ! grep -q "synology" /proc/version 2>/dev/null; then
        warning "Возможно, вы запускаете не на Synology NAS"
        read -p "Продолжить? (y/N): " continue_setup
        if [[ ! $continue_setup =~ ^[Yy]$ ]]; then
            echo "Настройка отменена"
            exit 1
        fi
    else
        success "Обнаружен Synology NAS"
    fi
}

# Создание .env файла
create_env_file() {
    if [ -f .env ]; then
        warning ".env файл уже существует"
        read -p "Перезаписать? (y/N): " overwrite
        if [[ ! $overwrite =~ ^[Yy]$ ]]; then
            info "Используем существующий .env файл"
            return
        fi
    fi
    
    echo ""
    info "Настройка переменных окружения..."
    echo ""
    
    # Запрос токена бота
    while true; do
        read -p "Введите токен Telegram бота: " bot_token
        if [[ -n "$bot_token" && $bot_token =~ ^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$ ]]; then
            break
        else
            error "Неверный формат токена! Пример: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        fi
    done
    
    # Запрос Admin ID
    while true; do
        read -p "Введите ваш Telegram ID (админ): " admin_id
        if [[ $admin_id =~ ^[0-9]+$ ]] && [ ${#admin_id} -ge 6 ]; then
            break
        else
            error "Admin ID должен быть числом (6+ цифр)"
            info "Найти свой ID: напишите @userinfobot в Telegram"
        fi
    done
    
    # Выбор часового пояса
    echo ""
    echo "Выберите часовой пояс:"
    echo "1) Europe/Moscow (UTC+3)"
    echo "2) Europe/Kiev (UTC+2)" 
    echo "3) Asia/Almaty (UTC+6)"
    echo "4) Asia/Tashkent (UTC+5)"
    echo "5) Другой (введите вручную)"
    
    read -p "Выберите (1-5) [1]: " tz_choice
    tz_choice=${tz_choice:-1}
    
    case $tz_choice in
        1) timezone="Europe/Moscow" ;;
        2) timezone="Europe/Kiev" ;;
        3) timezone="Asia/Almaty" ;;
        4) timezone="Asia/Tashkent" ;;
        5) 
            read -p "Введите часовой пояс (например, Europe/London): " timezone
            ;;
        *) timezone="Europe/Moscow" ;;
    esac
    
    # Создание .env файла
    cat > .env << EOF
# Telegram Bot Configuration
BOT_TOKEN=$bot_token
ADMIN_ID=$admin_id

# Python Configuration  
PYTHONUNBUFFERED=1

# Timezone Configuration
TZ=$timezone

# Optional: Database Configuration (раскомментируйте при необходимости)
# DB_HOST=postgres
# DB_NAME=school_bot
# DB_USER=bot_user
# DB_PASSWORD=secure_password_here

# Optional: Redis Configuration (раскомментируйте при необходимости) 
# REDIS_URL=redis://redis:6379/0
EOF

    chmod 600 .env
    success ".env файл создан и настроен"
}

# Выбор конфигурации Docker Compose
choose_configuration() {
    echo ""
    echo "Выберите конфигурацию развертывания:"
    echo ""
    echo "1) 🐳 Только бот (рекомендуется для начала)"
    echo "   - Минимальные ресурсы"
    echo "   - Быстрый запуск"
    echo ""
    echo "2) 🗄️ Бот + База данных PostgreSQL"
    echo "   - Для хранения пользовательских данных"
    echo "   - Больше возможностей"
    echo ""
    echo "3) 🚀 Полная конфигурация (Бот + DB + Redis + Nginx)"
    echo "   - Максимальная производительность"
    echo "   - Веб-интерфейс"
    echo ""
    
    read -p "Выберите конфигурацию (1-3) [1]: " config_choice
    config_choice=${config_choice:-1}
    
    case $config_choice in
        1)
            COMPOSE_FILE="docker-compose.synology.yml"
            info "Выбрана базовая конфигурация"
            ;;
        2)
            COMPOSE_FILE="docker-compose.synology.yml"
            info "Выбрана конфигурация с базой данных"
            warning "Не забудьте раскомментировать PostgreSQL секцию в docker-compose файле"
            ;;
        3)
            COMPOSE_FILE="docker-compose.synology.yml"
            info "Выбрана полная конфигурация"
            warning "Не забудьте раскомментировать дополнительные сервисы"
            ;;
        *)
            error "Неверный выбор, используем базовую конфигурацию"
            COMPOSE_FILE="docker-compose.synology.yml"
            ;;
    esac
    
    echo "COMPOSE_FILE=$COMPOSE_FILE" > .deploy-config
}

# Проверка ресурсов системы
check_resources() {
    echo ""
    info "Проверка системных ресурсов..."
    
    # Проверка RAM
    total_ram=$(free -m | awk 'NR==2{printf "%.0f", $2}')
    if [ "$total_ram" -lt 512 ]; then
        warning "Мало RAM: ${total_ram}MB. Рекомендуется минимум 512MB"
    else
        success "RAM: ${total_ram}MB - достаточно"
    fi
    
    # Проверка свободного места
    free_space=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$free_space" -lt 2 ]; then
        warning "Мало свободного места: ${free_space}GB. Рекомендуется минимум 2GB"
    else
        success "Свободное место: ${free_space}GB - достаточно"
    fi
}

# Создание необходимых директорий
setup_directories() {
    info "Создание рабочих директорий..."
    
    mkdir -p logs
    mkdir -p data
    mkdir -p backups
    
    chmod 755 logs data backups
    
    success "Директории созданы"
}

# Настройка автозапуска (только для Synology)
setup_autostart() {
    if ! grep -q "synology" /proc/version 2>/dev/null; then
        info "Автозапуск настраивается только на Synology NAS"
        return
    fi
    
    echo ""
    read -p "Настроить автозапуск при загрузке системы? (Y/n): " setup_auto
    setup_auto=${setup_auto:-y}
    
    if [[ $setup_auto =~ ^[Yy]$ ]]; then
        info "Создание скрипта автозапуска..."
        
        # Создание скрипта автозапуска
        cat > start-school-bot.sh << 'EOF'
#!/bin/bash
cd /volume1/docker/school-bot
docker-compose -f docker-compose.synology.yml up -d
EOF
        
        chmod +x start-school-bot.sh
        
        warning "Для автозапуска добавьте следующую команду в Control Panel > Task Scheduler:"
        echo "bash /volume1/docker/school-bot/start-school-bot.sh"
        
        success "Скрипт автозапуска создан"
    fi
}

# Финальная проверка
final_check() {
    echo ""
    info "Финальная проверка конфигурации..."
    
    # Проверка файлов
    local files=("Dockerfile" "docker-compose.synology.yml" "requirements.txt" "main.py" ".env")
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            success "$file найден"
        else
            error "$file отсутствует!"
            return 1
        fi
    done
    
    # Проверка переменных в .env
    if grep -q "your_bot_token_here" .env; then
        error "BOT_TOKEN не настроен в .env!"
        return 1
    fi
    
    if grep -q "your_admin_id_here" .env; then
        error "ADMIN_ID не настроен в .env!"
        return 1
    fi
    
    success "Все проверки пройдены!"
    return 0
}

# Показ инструкций по запуску
show_instructions() {
    echo ""
    echo "🎉 Настройка завершена!"
    echo "======================"
    echo ""
    echo "📝 Следующие шаги:"
    echo ""
    echo "1️⃣  Запуск бота:"
    echo "   bash deploy-synology.sh"
    echo ""
    echo "2️⃣  Проверка логов:"
    echo "   docker logs school-bot -f"
    echo ""
    echo "3️⃣  Остановка:"
    echo "   bash deploy-synology.sh --stop"
    echo ""
    echo "4️⃣  Container Manager:"
    echo "   http://$(hostname -I | awk '{print $1}'):5000"
    echo ""
    echo "📚 Документация:"
    echo "   - SYNOLOGY_DEPLOYMENT.md - полное руководство"
    echo "   - DOCKER_GUIDE.md - работа с Docker"
    echo "   - WEB_INTEGRATION.md - веб-функции бота"
    echo ""
    
    read -p "Запустить бота сейчас? (Y/n): " start_now
    start_now=${start_now:-y}
    
    if [[ $start_now =~ ^[Yy]$ ]]; then
        echo ""
        info "Запуск бота..."
        if [ -f deploy-synology.sh ]; then
            bash deploy-synology.sh
        else
            error "deploy-synology.sh не найден!"
        fi
    fi
}

# Основная функция
main() {
    check_synology
    create_env_file
    choose_configuration
    check_resources
    setup_directories
    setup_autostart
    
    if final_check; then
        show_instructions
    else
        error "Настройка не завершена из-за ошибок"
        exit 1
    fi
}

# Запуск
main