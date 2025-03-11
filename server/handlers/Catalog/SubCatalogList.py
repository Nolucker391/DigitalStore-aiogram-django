from aiogram import types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto, FSInputFile

from handlers.routes import router, logger
from aiogram.fsm.context import FSMContext

from keyboards.catalog.keyboard import apple_builder, sony_builder, samsung_builder

from states.history_static import set_user_state
from states.states import UserState

@router.callback_query(F.data.in_({'AppleCat', 'SonyCat', 'SamsungCat'}))
async def category_selection(callback: types.CallbackQuery, state: FSMContext):
    """ Доступные товары от определенного бренда."""

    logger.info(f"Пользователь: {callback.from_user.first_name} выбрал раздел Каталога - {callback.data}.")

    category_map = {
        'AppleCat': ('server/assets/images/catalog.png', '🍏 Apple', apple_builder()),
        'SonyCat': ('server/assets/images/catalog.png', '👾 Sony', sony_builder()),
        'SamsungCat': ('server/assets/images/catalog.png', '🕋 Samsung', samsung_builder())
    }

    file_path, caption, builder = category_map[callback.data]

    await state.update_data(main_category=callback)

    try:
        await set_user_state(state, UserState.product_type_selection)
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=FSInputFile(file_path),
                caption=f'🛍️Каталог -> {caption}:'
            ),
            reply_markup=builder.as_markup()
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return
        else:
            raise