from aiogram import types, F
from aiogram.types import FSInputFile, InputMediaPhoto

from handlers.DefaultCommands.StartCommand import set_user_state
from handlers.routes import router, logger
from aiogram.fsm.context import FSMContext
from states.states import UserState
from keyboards.catalog.CategoriesBuilder import cat_builder

@router.callback_query(F.data == 'first_block')
async def section_shop(callback: types.CallbackQuery, state: FSMContext):
    """Список товаров в магазине."""
    builder = cat_builder()
    file_path = "server/assets/images/catalog.png"

    logger.info(f"Пользователь: {callback.from_user.first_name} выбрал раздел Каталога.")

    await set_user_state(state, UserState.first_section)
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(file_path),  # Новый путь к фото
            caption='📋Список доступных ассортиментов.'
        ),
        reply_markup=builder.as_markup()  # Обновленные кнопки (если нужны)
    )