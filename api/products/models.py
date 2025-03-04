from django.db import models

from django.db import models


class Category(models.Model):
    """ Основные и вложенные категории """
    name = models.CharField(max_length=255, unique=True, verbose_name="Категория")
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
        verbose_name="Родительская категория"
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"  # Например: "Компьютеры → Игровые"
        return self.name  # Например: "Компьютеры"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    """ Модель продукта, привязанная к категории """
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        app_label = 'products'
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    """
    Функция для генерации пути сохранения фото продукта.
    Учитывает вложенность категорий.
    """
    category_path = instance.product.category.name.lower()

    # Проверяем, есть ли родительская категория
    if instance.product.category.parent:
        parent_category_path = instance.product.category.parent.name.lower()
        category_path = f"{parent_category_path}/{category_path}"

    return f"products/{category_path}/product_{instance.product.id}/{filename}"


class ProductImage(models.Model):
    """ Фото продукта """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_images_directory_path, verbose_name="Фото")

    class Meta:
        verbose_name = "Фото продукта"
        verbose_name_plural = "Фото продуктов"

# class Category(models.Model):
#     name = models.CharField(max_length=255, unique=True, verbose_name="Категория")
#     parent = models.ForeignKey(
#         "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="subcategories", verbose_name="Родительская категория"
#     )
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "Категория"
#         verbose_name_plural = "Категории"
#
#
# class Product(models.Model):
#     name = models.CharField(max_length=255, verbose_name="Название")
#     description = models.TextField(blank=True, null=True, verbose_name="Описание")
#     price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
#
#     def __str__(self):
#         return f"{self.name} ({self.category.name})"
#
#     class Meta:
#         app_label = 'products'
#         verbose_name = "Продукт"
#         verbose_name_plural = "Продукты"
#
#
# def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
#     """
#     Функция для сохранения пути фотографии, в директории.
#     """
#     return f"products/{instance.product.category.name.lower()}/product_{instance.product.id}/{filename}"
#
#
#
# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
#     image = models.ImageField(upload_to=product_images_directory_path, verbose_name="Фото")
#
#     class Meta:
#         verbose_name = "Фото продукта"
#         verbose_name_plural = "Фото продуктов"
#
#





#
# class Product(models.Model):
#     name = models.CharField(max_length=255, verbose_name="Название")
#     description = models.TextField(blank=True, null=True, verbose_name="Описание")
#     price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
#
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         app_label = 'products'
#         verbose_name = "Продукт"
#         verbose_name_plural = "Продукты"
#
# def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
#     """
#     Функция для сохранения пути фотографии, в директории.
#     """
#     return f"products/product_{instance.product.id}/{filename}"
#
#
# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
#     image = models.ImageField(upload_to=product_images_directory_path, verbose_name="Фото")
#
#     class Meta:
#         verbose_name = "Фото продукта"
#         verbose_name_plural = "Фото продуктов"