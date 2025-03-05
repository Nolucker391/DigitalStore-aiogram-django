from aiogram import types
from aiogram.types import Message, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart, Command
from asgiref.sync import sync_to_async
from keyboards.faq.faq_list import faq_list_questins
from handlers.routes import router, logger
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import CallbackQuery

from states.states import UserState
from states.history_static import set_user_state

@router.callback_query(F.data == 'third_block')
async def section_shop(callback: types.CallbackQuery, state: FSMContext):
    logger.info(f"Пользователь: {callback.from_user.first_name} выбрал раздел FAQ.")
    builder = faq_list_questins()
    file_path = "server/assets/images/faq.png"

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(file_path),  # Новый путь к фото
            caption='Ответы на частозадаваемые вопросы.'
        ),
        reply_markup=builder.as_markup()  # Обновленные кнопки (если нужны)
    )