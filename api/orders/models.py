from django.db import models

class Order(models.Model):
    """Модель заказа."""
    telegram_id = models.BigIntegerField()
    full_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[("Ожидание", "Ожидание"), ("Оплачен", "Оплачен")], default="Ожидание")

    def __str__(self):
        return f"Заказ #{self.id} от {self.full_name}"
