# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Указываем PYTHONPATH
ENV PYTHONPATH="/app"

# Запускаем несколько процессов с помощью supervisord
CMD ["bash", "-c", "cd api && python manage.py migrate && exec python manage.py runserver 0.0.0.0:8000"]
