from aiogram import types, F
from handlers.routes import router, logger
from aiogram.fsm.context import FSMContext

from states.history_static import set_user_state
from states.states import UserState

from ..utils.product_process import get_subcategory_products, update_product_message

@router.callback_query(F.data == 'Windows')
async def show_gaming_pc_with_cart(callback: types.CallbackQuery, state: FSMContext):
    """ Показывает товары из подкатегории 'Игровые компьютеры', если она принадлежит категории 'Компьютеры' """
    await set_user_state(state, UserState.select_gaming_pc)
    logger.info(f"Пользователь: {callback.from_user.first_name} выбрал раздел Моноблоки/Windows")

    products = await get_subcategory_products("моноблоки", "виндовс")  # Получаем товары

    if not products:
        await callback.answer("❌ В подкатегории 'Моноблоки/Windows' пока нет товаров.")
        return

    # Записываем список товаров и текущий индекс в FSMContext
    await state.update_data(products=products, product_index=0)

    await update_product_message(callback, state)  # Вызываем функцию обновления сообщения



