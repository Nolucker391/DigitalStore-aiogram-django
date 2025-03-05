from aiogram import types
from aiogram.filters import Command
from handlers.routes import router, logger
from aiogram.fsm.context import FSMContext

@router.message()
async def echo_message(message: types.Message):
    """
    Данная функция эхо-ответчик:
    - отвечает пользователю тем же сообщением, что он написал
    """
    await message.reply("Я вас не понимаю. Выберите что-то из меню.")



