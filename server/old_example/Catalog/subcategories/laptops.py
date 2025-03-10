from keyboards.catalog.sub_cat.LaptopsBuilder import laptop_builder


from aiogram import types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto, FSInputFile
from asgiref.sync import sync_to_async

from handlers.routes import router, logger
from aiogram.fsm.context import FSMContext

from states.history_static import set_user_state
from states.states import UserState
from keyboards.catalog.sub_cat.ComputersBuilder import computer_builder, build_navigation_keyboard
from products.models import Product, Category


@router.callback_query(F.data == 'laptops')
async def laptops_selection(callback: types.CallbackQuery, state: FSMContext):
    builder = laptop_builder()
    file_path = "server/assets/images/laptops.png"

    logger.info(f"Пользователь: {callback.from_user.first_name} выбрал раздел Ноутбуков.")

    try:
        await set_user_state(state, UserState.select_laptops)
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=FSInputFile(file_path),  # Новый путь к фото
                caption="Выберите интересующую модель.🪬"
            ),
            reply_markup=builder.as_markup()  # Обновленные кнопки (если нужны)
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return
        else:
            raise

