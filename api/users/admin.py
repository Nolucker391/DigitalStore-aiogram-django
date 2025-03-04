from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("tg_id", "username", "first_name", "created_at")
    search_fields = ("tg_id", "username", "first_name")
