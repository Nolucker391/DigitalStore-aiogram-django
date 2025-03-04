import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")  # Замените your_project на имя проекта
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = "admin"
EMAIL = "admin@example.com"
PASSWORD = "123"

if not User.objects.filter(username=USERNAME).exists():
    print("Создаю суперпользователя...")
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print("Суперпользователь создан!")
else:
    print("Суперпользователь уже существует.")
