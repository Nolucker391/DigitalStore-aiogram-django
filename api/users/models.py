from django.db import models


class User(models.Model):
    tg_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Username")
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self):
        return f"{self.first_name} (@{self.username})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
