from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers.DefaultCommands.StartCommand import start_command
from handlers.Catalog.CatalogList import section_shop
from handlers.Catalog.SubCatalogList import category_selection
from handlers.Catalog.ProductsList import show_products
from handlers.Basket.show_basket import show_user_cart
from handlers.Basket.change_basket_item import show_selected_product
from handlers.routes import router

from states.states import UserState


@router.callback_query(F.data == 'back')
async def back_to_previous_state(callback: CallbackQuery, state: FSMContext):
    """Возвращает пользователя к предыдущему состоянию"""
    data = await state.get_data()
    history = data.get("history", [])

    print(f"История состояний перед возвратом: {history}")

    if len(history) > 1:
        current_state_name = history.pop()
        previous_state_name = history[-1]
        previous_state = getattr(UserState, previous_state_name.split(":")[-1],
                                 UserState.start_section)
    else:
        previous_state_name = "UserState:start_section"
        previous_state = UserState.start_section

    await state.update_data(history=history)
    await state.set_state(previous_state)

    print(f"Переход к состоянию: {previous_state_name}")

    if previous_state_name == UserState.start_section:
        await start_command(callback, state)
        await callback.answer("Вы вернулись в главное меню.")
    elif previous_state_name == UserState.catalog_selection:
        await section_shop(callback, state)
    elif previous_state_name == UserState.product_type_selection:
        user_data = await state.get_data()
        main_category = user_data.get("main_category")
        await category_selection(main_category, state)
    elif previous_state_name == UserState.product_selection:
        user_data = await state.get_data()
        sub_category = user_data.get("sub_category")
        await show_products(sub_category, state)

    elif previous_state_name == UserState.basket_section:
        await show_user_cart(callback, state)  # Возвращаем к корзине
    elif previous_state_name == UserState.basket_item_select:
        await show_selected_product(callback, state)  # Возвращаем к выбранному товару