from django.db import models
from users.models import User

class Mailing(models.Model):
    message = models.TextField(verbose_name="Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Рассылка #{self.id} ({self.created_at})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
