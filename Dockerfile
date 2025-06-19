# Используем официальный образ Python (например, 3.11 slim)
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости (предположим, у вас есть requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска вашего бота
CMD ["python", "-u", "main.py"]
