from aiogram import types, F
from aiogram.types import InputMediaPhoto, FSInputFile

from handlers.routes import router
from aiogram.fsm.context import FSMContext

from states.history_static import set_user_state
from states.states import UserState
from keyboards.catalog.sub_cat.MonoBuilder import monoblock_bluider

@router.callback_query(F.data == 'monoblocks')
async def monoblock_selection(callback: types.CallbackQuery, state: FSMContext):
    builder = monoblock_bluider()
    file_path = "bot/assets/images/monoblocks.png"

    await set_user_state(state, UserState.select_monoblocks)
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(file_path),  # Новый путь к фото
            caption="Выберите интересующую модель.🪬."
        ),
        reply_markup=builder.as_markup()  # Обновленные кнопки (если нужны)
    )