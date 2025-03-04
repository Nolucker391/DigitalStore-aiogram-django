from aiogram import types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto, FSInputFile

from handlers.routes import router, logger
from aiogram.fsm.context import FSMContext

from states.history_static import set_user_state
from states.states import UserState
from keyboards.catalog.sub_cat.ComputersBuilder import computer_builder, build_navigation_keyboard


@router.callback_query(F.data == 'computers')
async def computer_selection(callback: types.CallbackQuery, state: FSMContext):
    """Выбор категории Компьютеры"""
    builder = computer_builder()
    file_path = "server/assets/images/computers.png"

    logger.info(f"Пользователь: {callback.from_user.first_name} выбрал раздел Компьютеры.")

    try:
        await set_user_state(state, UserState.select_computer)
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=FSInputFile(file_path),
                caption="Выберите интересующую подкатегорию 🖥"
            ),
            reply_markup=builder.as_markup()
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return
        else:
            raise


@router.callback_query(F.data.in_(["prev_product", "next_product"]))
async def change_product(callback: types.CallbackQuery, state: FSMContext):
    """ Листает товары вперёд и назад """
    data = await state.get_data()
    index = data.get("product_index", 0)
    products = data.get("products", [])

    if callback.data == "next_product" and index < len(products) - 1:
        index += 1
    elif callback.data == "prev_product" and index > 0:
        index -= 1

    await state.update_data(product_index=index)  # Обновляем индекс товара
    await update_product_message(callback, state)  # Обновляем сообщение