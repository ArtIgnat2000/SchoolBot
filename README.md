# 🐍 Инструкции по настройке виртуального окружения

## Создание виртуального окружения

### Windows (PowerShell):
```powershell
# Перейти в папку проекта
cd "d:\TG_Bots\School_Bot"

# Создать виртуальное окружение
python -m venv venv

# Активировать окружение
.\venv\Scripts\Activate.ps1

# Если возникает ошибка с политикой выполнения, выполните:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows (Command Prompt):
```cmd
# Перейти в папку проекта
cd "d:\TG_Bots\School_Bot"

# Создать виртуальное окружение
python -m venv venv

# Активировать окружение
venv\Scripts\activate.bat
```

### Linux/macOS:
```bash
# Перейти в папку проекта
cd /path/to/School_Bot

# Создать виртуальное окружение
python3 -m venv venv

# Активировать окружение
source venv/bin/activate
```

## Установка зависимостей

После активации виртуального окружения:

```bash
# Обновить pip
python -m pip install --upgrade pip

# Установить зависимости из requirements.txt
pip install -r requirements.txt

# Или установить вручную
pip install aiogram==3.13.1 python-dotenv==1.0.1 aiofiles==24.1.0
```

## Проверка установки

```bash
# Проверить установленные пакеты
pip list

# Проверить версию Python
python --version

# Проверить aiogram
python -c "import aiogram; print(aiogram.__version__)"
```

## Деактивация окружения

```bash
deactivate
```

## Настройка переменных окружения

1. Скопируйте файл `.env.example` в `.env`
2. Заполните необходимые переменные:
   - `BOT_TOKEN` - токен вашего бота от @BotFather
   - `ADMIN_IDS` - ID администраторов через запятую

## Запуск бота

```bash
# Убедитесь, что виртуальное окружение активировано
# Должно быть видно (venv) в начале строки терминала

# Запустить бота
python main.py
```

## Полезные команды

```bash
# Сохранить текущие зависимости
pip freeze > requirements.txt

# Очистить кэш pip
pip cache purge

# Показать информацию о пакете
pip show aiogram
```

## Возможные проблемы и решения

### 1. Ошибка активации в PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Python не найден
- Убедитесь, что Python установлен
- Проверьте PATH переменные
- Используйте `python3` вместо `python` на Linux/macOS

### 3. Ошибки при установке пакетов
```bash
# Обновить pip и setuptools
python -m pip install --upgrade pip setuptools

# Очистить кэш
pip cache purge
```