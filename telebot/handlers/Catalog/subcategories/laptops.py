from aiogram import types, F
from aiogram.types import InputMediaPhoto, FSInputFile

from states.history_static import set_user_state
from handlers.routes import router
from aiogram.fsm.context import FSMContext
from states.states import UserState
from keyboards.catalog.sub_cat.LaptopsBuilder import laptop_builder

@router.callback_query(F.data == 'laptops')
async def laptops_selection(callback: types.CallbackQuery, state: FSMContext):
    builder = laptop_builder()
    file_path = "bot/assets/images/laptops.png"

    await set_user_state(state, UserState.select_laptops)
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(file_path),  # Новый путь к фото
            caption="Выберите интересующую модель.🪬"
        ),
        reply_markup=builder.as_markup()  # Обновленные кнопки (если нужны)
    )