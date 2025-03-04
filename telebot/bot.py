import os
import django
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "api"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.api.settings')
django.setup()

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
import asyncio
from config.config_reader import config
from handlers.routes import router

bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode="HTML"))


async def main():
    dp = Dispatcher()

    dp.include_routers(
        router
    )
    await bot.delete_webhook(drop_pending_updates=True) #Удаляем накопленные сообщения, если бот был выкл, а его пытались использовать
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())