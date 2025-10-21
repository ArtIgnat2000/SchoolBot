#!/bin/bash

# Быстрое исправление прав Docker для Synology NAS
# Автор: @Vprog2

echo "🔧 Synology Docker Permissions Fix"
echo "=================================="
echo ""

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Проверка текущего доступа к Docker
check_docker_access() {
    info "Проверка доступа к Docker..."
    
    if docker info &> /dev/null; then
        success "Docker доступен без sudo"
        return 0
    elif sudo docker info &> /dev/null; then
        warning "Docker доступен только через sudo"
        return 1
    else
        error "Docker недоступен"
        return 2
    fi
}

# Попытка исправления прав
fix_permissions() {
    info "Попытка исправления прав..."
    
    # Способ 1: chmod на socket (самый простой)
    if sudo chmod 666 /var/run/docker.sock 2>/dev/null; then
        success "Права на Docker socket изменены"
        if docker info &> /dev/null; then
            success "Docker теперь доступен без sudo!"
            return 0
        fi
    fi
    
    # Способ 2: Добавление в группу через разные команды
    info "Попытка добавления в группу docker..."
    
    # Проверяем доступность команд
    local user_added=false
    
    if command -v usermod &> /dev/null; then
        if sudo usermod -aG docker $USER 2>/dev/null; then
            success "Добавлен через usermod"
            user_added=true
        fi
    fi
    
    if ! $user_added && command -v adduser &> /dev/null; then
        if sudo adduser $USER docker 2>/dev/null; then
            success "Добавлен через adduser"
            user_added=true
        fi
    fi
    
    if ! $user_added && command -v synogroup &> /dev/null; then
        if sudo synogroup --add docker $USER 2>/dev/null; then
            success "Добавлен через synogroup (Synology)"
            user_added=true
        fi
    fi
    
    if $user_added; then
        warning "Необходимо перелогиниться для применения изменений в группах"
        info "Выполните: exit, затем подключитесь заново"
        return 0
    fi
    
    return 1
}

# Показать альтернативные решения
show_alternatives() {
    echo ""
    info "Альтернативные решения:"
    echo ""
    echo "1️⃣  Всегда использовать sudo:"
    echo "   sudo bash deploy-synology.sh"
    echo ""
    echo "2️⃣  Изменить права после каждой перезагрузки:"
    echo "   sudo chmod 666 /var/run/docker.sock"
    echo ""
    echo "3️⃣  Использовать Container Manager GUI:"
    echo "   - Откройте Container Manager в DSM"
    echo "   - Project → Create → укажите путь к проекту"
    echo "   - Выберите docker-compose.synology.yml"
    echo ""
    echo "4️⃣  Создать alias для sudo:"
    echo "   echo 'alias docker=\"sudo docker\"' >> ~/.bashrc"
    echo "   echo 'alias docker-compose=\"sudo docker-compose\"' >> ~/.bashrc"
    echo "   source ~/.bashrc"
}

# Основная функция
main() {
    case $(check_docker_access) in
        0)
            success "Docker работает нормально!"
            info "Можете использовать: bash deploy-synology.sh"
            exit 0
            ;;
        1)
            warning "Docker доступен только через sudo"
            echo ""
            read -p "Попробовать исправить автоматически? (Y/n): " fix_auto
            fix_auto=${fix_auto:-y}
            
            if [[ $fix_auto =~ ^[Yy]$ ]]; then
                if fix_permissions; then
                    success "Права исправлены!"
                    check_docker_access
                else
                    error "Автоматическое исправление не удалось"
                    show_alternatives
                fi
            else
                show_alternatives
            fi
            ;;
        2)
            error "Docker недоступен!"
            info "Убедитесь что Container Manager установлен и запущен"
            exit 1
            ;;
    esac
}

# Запуск
main