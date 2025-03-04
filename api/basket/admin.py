from django.contrib import admin
from .models import Basket

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "product", "count", "total_price")
    search_fields = ("telegram_id", "product__name")
