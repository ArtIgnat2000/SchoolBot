FROM python:3.11-slim

WORKDIR /app

# Копируем файлы зависимостей отдельно для лучшего кэширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Переменная окружения для Python
ENV PYTHONUNBUFFERED=1

# Запуск приложения (JSON формат для правильной обработки сигналов)
CMD ["python", "main.py"]
