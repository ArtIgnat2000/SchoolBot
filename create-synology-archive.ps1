# PowerShell скрипт для создания архива School Bot для Synology
# Автор: @Vprog2

Write-Host "🎓 Создание архива School Bot для Synology NAS..." -ForegroundColor Blue
Write-Host ""

# Проверка текущей директории
if (!(Test-Path "main.py")) {
    Write-Host "❌ Ошибка: main.py не найден. Запустите скрипт из папки проекта!" -ForegroundColor Red
    exit 1
}

# Список файлов для архива
$FilesToInclude = @(
    # Основные файлы проекта
    "main.py",
    "config.py", 
    "keyboards.py",
    "utils.py",
    "requirements.txt",
    
    # Docker файлы
    "Dockerfile",
    "Dockerfile.optimized",
    "docker-compose.yml",
    "docker-compose.synology.yml",
    ".dockerignore",
    
    # Скрипты для Synology
    "setup-synology.sh",
    "deploy-synology.sh",
    
    # Обработчики (папка)
    "handlers",
    
    # Документация
    "README.md",
    "SYNOLOGY_DEPLOYMENT.md", 
    "QUICK_START_SYNOLOGY.md",
    "DOCKER_GUIDE.md",
    "WEB_INTEGRATION.md",
    "CHANGELOG.md",
    
    # Конфигурация
    ".gitignore"
)

# Проверка существования файлов
Write-Host "🔍 Проверка файлов..." -ForegroundColor Yellow
$MissingFiles = @()
$ExistingFiles = @()

foreach ($file in $FilesToInclude) {
    if (Test-Path $file) {
        $ExistingFiles += $file
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        $MissingFiles += $file
        Write-Host "⚠️  $file (не найден)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "📊 Статистика:" -ForegroundColor Cyan
Write-Host "   Найдено файлов: $($ExistingFiles.Count)" -ForegroundColor Green
Write-Host "   Отсутствует файлов: $($MissingFiles.Count)" -ForegroundColor Yellow

if ($MissingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  Отсутствующие файлы будут пропущены:" -ForegroundColor Yellow
    foreach ($file in $MissingFiles) {
        Write-Host "   - $file" -ForegroundColor Yellow
    }
}

# Создание архива
$ArchiveName = "school-bot-synology-$(Get-Date -Format 'yyyy-MM-dd').zip"
Write-Host ""
Write-Host "📦 Создание архива: $ArchiveName" -ForegroundColor Blue

try {
    # Удаляем старый архив если существует
    if (Test-Path $ArchiveName) {
        Remove-Item $ArchiveName -Force
        Write-Host "🗑️  Удален старый архив" -ForegroundColor Yellow
    }
    
    # Создаем новый архив
    Compress-Archive -Path $ExistingFiles -DestinationPath $ArchiveName -CompressionLevel Optimal
    
    # Информация об архиве
    $ArchiveInfo = Get-Item $ArchiveName
    $SizeMB = [math]::Round($ArchiveInfo.Length / 1MB, 2)
    
    Write-Host ""
    Write-Host "🎉 Архив успешно создан!" -ForegroundColor Green
    Write-Host "📁 Файл: $ArchiveName" -ForegroundColor Cyan
    Write-Host "💾 Размер: $SizeMB MB" -ForegroundColor Cyan
    Write-Host "📂 Расположение: $(Get-Location)\$ArchiveName" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Ошибка при создании архива: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Инструкции по загрузке
Write-Host ""
Write-Host "📋 Следующие шаги:" -ForegroundColor Blue
Write-Host ""
Write-Host "1️⃣  Загрузите архив на Synology NAS:" -ForegroundColor White
Write-Host "   - Откройте File Station" -ForegroundColor Gray
Write-Host "   - Перейдите в /volume1/docker/" -ForegroundColor Gray
Write-Host "   - Создайте папку 'school-bot'" -ForegroundColor Gray
Write-Host "   - Загрузите и распакуйте $ArchiveName" -ForegroundColor Gray
Write-Host ""
Write-Host "2️⃣  Подключитесь по SSH к NAS:" -ForegroundColor White
Write-Host "   ssh admin@your_synology_ip" -ForegroundColor Gray
Write-Host ""
Write-Host "3️⃣  Перейдите в папку проекта:" -ForegroundColor White
Write-Host "   cd /volume1/docker/school-bot/" -ForegroundColor Gray
Write-Host ""
Write-Host "4️⃣  Запустите интерактивную настройку:" -ForegroundColor White
Write-Host "   bash setup-synology.sh" -ForegroundColor Gray
Write-Host ""
Write-Host "5️⃣  Разверните бота:" -ForegroundColor White
Write-Host "   bash deploy-synology.sh" -ForegroundColor Gray
Write-Host ""

# Открыть папку с архивом
$OpenFolder = Read-Host "Открыть папку с архивом? (y/N)"
if ($OpenFolder -eq "y" -or $OpenFolder -eq "Y") {
    Start-Process explorer.exe -ArgumentList (Get-Location)
}

Write-Host ""
Write-Host "✨ Готово! Архив готов для загрузки на Synology NAS." -ForegroundColor Green