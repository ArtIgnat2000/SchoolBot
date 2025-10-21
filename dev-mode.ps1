# Скрипт для управления режимами разработки School Bot

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("dev", "external", "prod", "stop", "status")]
    [string]$Mode
)

$ErrorActionPreference = "Stop"

function Write-Header {
    param([string]$Message)
    Write-Host "`n🤖 School Bot - $Message" -ForegroundColor Cyan
    Write-Host ("=" * 50) -ForegroundColor DarkCyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Yellow
}

function Stop-AllContainers {
    Write-Info "Останавливаю все контейнеры School Bot..."
    
    $containers = @(
        "docker-compose.yml",
        "docker-compose.dev.yml", 
        "docker-compose.external-code.yml"
    )
    
    foreach ($compose in $containers) {
        if (Test-Path $compose) {
            try {
                docker-compose -f $compose down 2>$null
            } catch {
                # Игнорируем ошибки, если контейнер не запущен
            }
        }
    }
    Write-Success "Все контейнеры остановлены"
}

function Get-ContainerStatus {
    Write-Header "Статус контейнеров"
    
    $containers = docker ps -a --filter "name=school-bot" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    if ($containers -match "school-bot") {
        Write-Host $containers
    } else {
        Write-Info "Контейнеры School Bot не найдены"
    }
    
    Write-Host "`n📊 Docker Compose статус:"
    
    $composeFiles = @(
        @{File="docker-compose.yml"; Name="Продакшн"},
        @{File="docker-compose.dev.yml"; Name="Разработка (авто-reload)"},
        @{File="docker-compose.external-code.yml"; Name="Внешний код"}
    )
    
    foreach ($compose in $composeFiles) {
        if (Test-Path $compose.File) {
            try {
                $status = docker-compose -f $compose.File ps --services 2>$null
                if ($status) {
                    Write-Host "  ✅ $($compose.Name): активен" -ForegroundColor Green
                } else {
                    Write-Host "  ⏸️  $($compose.Name): остановлен" -ForegroundColor Gray
                }
            } catch {
                Write-Host "  ❌ $($compose.Name): ошибка" -ForegroundColor Red
            }
        }
    }
}

switch ($Mode) {
    "dev" {
        Write-Header "Режим разработки (авто-reload)"
        Stop-AllContainers
        
        Write-Info "Запускаю контейнер с автоматическим перезапуском..."
        docker-compose -f docker-compose.dev.yml up -d
        
        Write-Success "Режим разработки активен!"
        Write-Host "`n📝 Особенности:" -ForegroundColor Yellow
        Write-Host "  • Код монтируется с хоста"
        Write-Host "  • Автоматический перезапуск при изменениях .py файлов"
        Write-Host "  • Отключено создание .pyc файлов"
        Write-Host "`n🔧 Команды:"
        Write-Host "  • Логи: docker-compose -f docker-compose.dev.yml logs -f"
        Write-Host "  • Подключение: docker exec -it school-bot-dev bash"
    }
    
    "external" {
        Write-Header "Режим внешнего кода"
        Stop-AllContainers
        
        Write-Info "Запускаю контейнер с монтированием кода..."
        docker-compose -f docker-compose.external-code.yml up -d
        
        Write-Success "Режим внешнего кода активен!"
        Write-Host "`n📝 Особенности:" -ForegroundColor Yellow
        Write-Host "  • Конкретные файлы монтируются с хоста"
        Write-Host "  • Ручной перезапуск после изменений"
        Write-Host "  • Простой и надежный подход"
        Write-Host "`n🔧 Команды:"
        Write-Host "  • Перезапуск: docker-compose -f docker-compose.external-code.yml restart"
        Write-Host "  • Логи: docker-compose -f docker-compose.external-code.yml logs -f"
    }
    
    "prod" {
        Write-Header "Продакшн режим"
        Stop-AllContainers
        
        Write-Info "Запускаю продакшн контейнер..."
        docker-compose up -d
        
        Write-Success "Продакшн режим активен!"
        Write-Host "`n📝 Особенности:" -ForegroundColor Yellow
        Write-Host "  • Код встроен в образ"
        Write-Host "  • Максимальная стабильность"
        Write-Host "  • Для обновления нужна пересборка образа"
        Write-Host "`n🔧 Команды:"
        Write-Host "  • Логи: docker-compose logs -f"
        Write-Host "  • Пересборка: docker-compose build --no-cache"
    }
    
    "stop" {
        Write-Header "Остановка всех контейнеров"
        Stop-AllContainers
        Write-Success "Все контейнеры School Bot остановлены"
    }
    
    "status" {
        Get-ContainerStatus
    }
}

Write-Host "`n🎯 Для получения статуса: .\dev-mode.ps1 status" -ForegroundColor Cyan