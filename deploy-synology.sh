#!/bin/bash

# Скрипт развертывания School Bot на Synology NAS
# Автор: @Vprog2
# Версия: 1.0

set -e  # Выход при любой ошибке

echo "🚀 Запуск развертывания School Bot на Synology..."

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка наличия Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker не найден! Установите Container Manager через Package Center."
        exit 1
    fi
    log_success "Docker найден"
}

# Проверка наличия docker-compose
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        log_warning "docker-compose не найден, попытка использовать docker compose..."
        if ! docker compose version &> /dev/null; then
            log_error "Ни docker-compose, ни docker compose не найдены!"
            exit 1
        fi
        COMPOSE_CMD="docker compose"
    else
        COMPOSE_CMD="docker-compose"
    fi
    log_success "Docker Compose найден: $COMPOSE_CMD"
}

# Создание необходимых директорий
create_directories() {
    log_info "Создание директорий..."
    mkdir -p logs
    chmod 755 logs
    log_success "Директории созданы"
}

# Проверка .env файла
check_env_file() {
    if [ ! -f .env ]; then
        log_warning ".env файл не найден, создание шаблона..."
        cat > .env << EOF
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id_here

# Python Configuration
PYTHONUNBUFFERED=1

# Timezone (измените на ваш)
TZ=Europe/Moscow
EOF
        chmod 600 .env
        log_error "⚠️  ВНИМАНИЕ: Отредактируйте .env файл с вашими данными!"
        log_error "Установите BOT_TOKEN и ADMIN_ID перед запуском."
        read -p "Нажмите Enter после редактирования .env файла..."
    else
        log_success ".env файл найден"
        
        # Проверка наличия обязательных переменных
        if ! grep -q "BOT_TOKEN=" .env || grep -q "BOT_TOKEN=your_bot_token_here" .env; then
            log_error "⚠️  BOT_TOKEN не настроен в .env файле!"
            exit 1
        fi
        
        if ! grep -q "ADMIN_ID=" .env || grep -q "ADMIN_ID=your_admin_id_here" .env; then
            log_error "⚠️  ADMIN_ID не настроен в .env файле!"
            exit 1
        fi
        
        log_success "Конфигурация .env проверена"
    fi
}

# Выбор Docker Compose файла
choose_compose_file() {
    echo ""
    echo "Выберите конфигурацию для развертывания:"
    echo "1) Базовая конфигурация (docker-compose.yml)"
    echo "2) Оптимизированная для Synology (docker-compose.synology.yml)"
    echo ""
    read -p "Введите номер (1-2) [2]: " choice
    choice=${choice:-2}
    
    case $choice in
        1)
            COMPOSE_FILE="docker-compose.yml"
            log_info "Выбрана базовая конфигурация"
            ;;
        2)
            COMPOSE_FILE="docker-compose.synology.yml"
            log_info "Выбрана конфигурация для Synology"
            ;;
        *)
            log_error "Неверный выбор!"
            exit 1
            ;;
    esac
}

# Остановка существующих контейнеров
stop_existing() {
    log_info "Остановка существующих контейнеров..."
    $COMPOSE_CMD -f $COMPOSE_FILE down --remove-orphans || true
    
    # Принудительная остановка если контейнер висит
    if docker ps | grep -q school-bot; then
        log_warning "Принудительная остановка контейнера school-bot..."
        docker stop school-bot || true
        docker rm school-bot || true
    fi
    
    log_success "Существующие контейнеры остановлены"
}

# Сборка образа
build_image() {
    log_info "Сборка Docker образа..."
    $COMPOSE_CMD -f $COMPOSE_FILE build --no-cache
    log_success "Образ собран успешно"
}

# Запуск контейнеров
start_containers() {
    log_info "Запуск контейнеров..."
    $COMPOSE_CMD -f $COMPOSE_FILE up -d
    log_success "Контейнеры запущены"
}

# Проверка статуса
check_status() {
    echo ""
    log_info "Статус контейнеров:"
    $COMPOSE_CMD -f $COMPOSE_FILE ps
    
    echo ""
    log_info "Проверка здоровья контейнера..."
    sleep 10
    
    if docker ps | grep -q school-bot; then
        log_success "✅ Контейнер school-bot запущен"
        
        # Проверка логов
        echo ""
        log_info "Последние логи:"
        docker logs school-bot --tail 20
        
    else
        log_error "❌ Контейнер school-bot не запущен!"
        log_error "Проверьте логи: docker logs school-bot"
        exit 1
    fi
}

# Функция показа помощи
show_help() {
    echo "Использование: $0 [опции]"
    echo ""
    echo "Опции:"
    echo "  -h, --help     Показать эту справку"
    echo "  -s, --stop     Остановить контейнеры"
    echo "  -r, --restart  Перезапустить контейнеры"
    echo "  -l, --logs     Показать логи"
    echo "  -u, --update   Обновить и перезапустить"
    echo ""
    echo "Примеры:"
    echo "  $0             # Полное развертывание"
    echo "  $0 --stop      # Остановка"
    echo "  $0 --restart   # Перезапуск"
    echo "  $0 --logs      # Просмотр логов"
}

# Обработка аргументов командной строки
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    -s|--stop)
        check_docker
        check_docker_compose
        choose_compose_file
        log_info "Остановка School Bot..."
        $COMPOSE_CMD -f $COMPOSE_FILE down
        log_success "School Bot остановлен"
        exit 0
        ;;
    -r|--restart)
        check_docker
        check_docker_compose
        choose_compose_file
        log_info "Перезапуск School Bot..."
        $COMPOSE_CMD -f $COMPOSE_FILE restart
        check_status
        exit 0
        ;;
    -l|--logs)
        check_docker
        log_info "Логи School Bot:"
        docker logs school-bot -f
        exit 0
        ;;
    -u|--update)
        check_docker
        check_docker_compose
        choose_compose_file
        log_info "Обновление School Bot..."
        stop_existing
        build_image
        start_containers
        check_status
        log_success "School Bot обновлен успешно!"
        exit 0
        ;;
esac

# Основной процесс развертывания
main() {
    echo "🎓 School Bot - Развертывание на Synology NAS"
    echo "=============================================="
    echo ""
    
    # Проверки
    check_docker
    check_docker_compose
    create_directories
    check_env_file
    choose_compose_file
    
    echo ""
    log_info "Начинаем развертывание..."
    
    # Развертывание
    stop_existing
    build_image
    start_containers
    check_status
    
    echo ""
    echo "🎉 School Bot успешно развернут!"
    echo ""
    echo "📋 Полезные команды:"
    echo "  Логи:        docker logs school-bot -f"
    echo "  Статус:      docker ps"
    echo "  Остановка:   $COMPOSE_CMD -f $COMPOSE_FILE down"
    echo "  Перезапуск:  $COMPOSE_CMD -f $COMPOSE_FILE restart"
    echo ""
    echo "🌐 Container Manager: http://$(hostname -I | awk '{print $1}'):5000"
    echo ""
    log_success "Развертывание завершено!"
}

# Запуск основной функции
main