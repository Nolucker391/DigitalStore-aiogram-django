from django.contrib import admin, messages
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.html import format_html
from .models import Mailing
from users.models import User
from aiogram import Bot
import asyncio
from api.settings import bot_token
from asgiref.sync import async_to_sync, sync_to_async
from aiogram.types import FSInputFile


bot = Bot(token=bot_token)

async def send_message_to_users(message):
    users = await sync_to_async(list)(User.objects.all())

    video_path = "mailing/content/video/mell.MP4"

    for user in users:
        try:
            # await bot.send_message(chat_id=user.tg_id, text=message)
            # await bot.send_video(
            #     chat_id=user.tg_id,
            #     video=FSInputFile(video_path),
            #     caption="🪬Приуэт, мои любимые подоконники, подпэсщнэки.💅"
            # )

            await bot.send_video(
                chat_id=user.tg_id,
                video=FSInputFile(video_path),
                caption=message,
            )
        except Exception as e:
            print(f"Ошибка отправки пользователю {user.tg_id}: {e}")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ["id", "message", "created_at", "send_messages"]
    readonly_fields = ["created_at"]

    def send_messages(self, obj):
        url = reverse("admin:send_mailing", args=[obj.id])
        return format_html('<a class="button" href="{}">📨 Отправить</a>', url)

    send_messages.short_description = "Отправить рассылку"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:mailing_id>/send/', self.admin_site.admin_view(self.send_mailing_view), name="send_mailing"),
        ]
        return custom_urls + urls

    def send_mailing_view(self, request, mailing_id):
        mailing = Mailing.objects.get(id=mailing_id)
        async_to_sync(send_message_to_users)(mailing.message)
        messages.success(request, "✅ Рассылка успешно отправлена!")
        return redirect(request.META.get("HTTP_REFERER", "/admin/mailing/mailing/"))
