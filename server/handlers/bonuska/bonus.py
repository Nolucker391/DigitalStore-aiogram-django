from handlers.routes import router, logger
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile, InputMediaPhoto


@router.callback_query(F.data == "Four")
async def bonus_section(callback: types.CallbackQuery, state: FSMContext):
    """Пользователь выбрал бонусынй раздел."""
    builder_inline = InlineKeyboardBuilder()

    builder_inline.row(
        types.InlineKeyboardButton(text="Почему же?", callback_data="why")
    )

    file_path = "server/assets/images/bonuska.png"
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(file_path),
            caption="🤔Знаете почему я выбрал <b>Вас?</b>"
        ),
        reply_markup=builder_inline.as_markup()
    )

@router.callback_query(F.data == "why")
async def video_section(callback: types.CallbackQuery, state: FSMContext):
    """Отправка видео с сообщением."""
    await callback.message.delete()

    builder_inline = InlineKeyboardBuilder()

    builder_inline.row(
        types.InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="back_to_menu")
    )

    video_path = "server/assets/video/krasava.MP4"

    await callback.message.answer_video(
        video=types.FSInputFile(video_path),
        reply_markup=builder_inline.as_markup()
    )