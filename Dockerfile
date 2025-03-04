# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Добавляем PYTHONPATH
ENV PYTHONPATH="/app"

# Команда по умолчанию будет переопределена в docker-compose
CMD ["bash", "-c", "cd api && python manage.py migrate && python manage.py runserver & python server/bot.py"]
