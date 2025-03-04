from django.db import models
from products.models import Product

class Basket(models.Model):
    """Корзина пользователя."""
    telegram_id = models.BigIntegerField(verbose_name="Telegram ID")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="baskets")
    count = models.PositiveIntegerField(default=1, verbose_name="Количество")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")

    class Meta:
        app_label = 'basket'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        unique_together = ('telegram_id', 'product')  # Каждый товар уникален для пользователя

    def save(self, *args, **kwargs):
        self.total_price = self.count * self.product.price  # Пересчитываем сумму
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.count} шт."
