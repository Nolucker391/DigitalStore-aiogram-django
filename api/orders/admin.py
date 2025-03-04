from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Настройки модели Order в Django Admin.
    Также выгрузка данных в exel-формат
    """
    list_display = ("id", "telegram_id", "full_name", "status")  # Отображаемые колонки
    list_filter = ("status",)  # Фильтрация по статусу
    search_fields = ("telegram_id", "full_name")  # Поиск по полям
    ordering = ("-id",)  # Сортировка заказов (новые сверху)
    actions = ["export_to_excel"]  # Добавляем кастомное действие

    @admin.action(description="📥 Скачать заказы в Excel")
    def export_to_excel(self, request, queryset):
        """Экспорт заказов в Excel."""
        wb = Workbook()  # Создаем новую книгу Excel
        ws = wb.active
        ws.title = "Orders"

        # Заголовки столбцов
        headers = ["ID", "Telegram ID", "ФИО", "Статус"]
        ws.append(headers)

        # Заполняем таблицу данными
        for order in Order.objects.all():
            ws.append([order.id, order.telegram_id, order.full_name, order.status])

        # Создаем HTTP-ответ с файлом Excel
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="orders.xlsx"'
        wb.save(response)
        return response
