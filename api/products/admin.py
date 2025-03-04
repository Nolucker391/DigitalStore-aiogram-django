from django.contrib import admin
from .models import Category, Product, ProductImage


class CategoryAdmin(admin.ModelAdmin):
    """ Админка для категорий """
    list_display = ("name", "parent")  # Показываем имя категории и её родителя
    search_fields = ("name",)  # Поиск по названию категории
    list_filter = ("parent",)  # Фильтр по родительским категориям
    ordering = ["parent__name", "name"]  # Сортировка по родителю, затем по имени

    def get_queryset(self, request):
        """ Оптимизация запросов для категорий """
        return super().get_queryset(request).select_related("parent")


class ProductImageInline(admin.TabularInline):
    """ Встроенный показ фото в карточке продукта """
    model = ProductImage
    extra = 1  # Количество пустых полей для загрузки фото


class ProductAdmin(admin.ModelAdmin):
    """ Админка для товаров """
    list_display = ("name", "category", "price", "created_at")  # Добавил категорию
    search_fields = ("name", "category__name")  # Поиск по названию и категории
    list_filter = ("category",)  # Фильтр по категориям
    inlines = [ProductImageInline]  # Показываем изображения прямо в продукте
    ordering = ["-created_at"]  # Сортировка по дате добавления (сначала новые)

    def get_queryset(self, request):
        """ Оптимизация запросов для товаров """
        return super().get_queryset(request).select_related("category")


class ProductImageAdmin(admin.ModelAdmin):
    """ Админка для фото товаров """
    list_display = ("product", "image")


# Регистрируем модели в админке
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)




# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'description', 'created_at')
#     search_fields = ('name',)

# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ('product', 'image')
#     search_fields = ('name',)



# class ProductImageInline(admin.TabularInline):  # Встроенный показ фото в карточке продукта
#     model = ProductImage
#     extra = 1  # Количество пустых полей для загрузки фото
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'created_at')  # Убрано описание, чтобы не загромождало
#     search_fields = ('name',)
#     inlines = [ProductImageInline]  # Показываем изображения прямо в продукте
#
# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ('product', 'image')