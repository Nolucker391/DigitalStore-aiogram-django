from aiogram import F
from aiogram.types import CallbackQuery

# from handlers.Catalog.subcategories.computers import computer_selection
# from handlers.Catalog.subcategories.gaming.gaming_comp import show_gaming_pc_with_cart
# from handlers.Catalog.subcategories.laptops import laptops_selection
# from handlers.Catalog.subcategories.monoblocks import monoblock_selection
from handlers.DefaultCommands.StartCommand import start_command

from handlers.Catalog.AppleCat import category_selection
from handlers.Catalog.main import section_shop
from handlers.Catalog.Accessories import show_products
from handlers.Catalog.prod import show_product_details

from handlers.Basket.show_basket import show_user_cart
from handlers.Basket.change_basket_item import show_selected_product
from handlers.routes import router
from aiogram.fsm.context import FSMContext

from states.states import UserState


# @router.callback_query(F.data == 'back')
# async def back_to_previous_state(callback: CallbackQuery, state: FSMContext):
#     """Возвращает пользователя к предыдущему состоянию"""
#     data = await state.get_data()
#     history = data.get("history", [])
#     print(f"История состояний перед возвратом: {history}")  # Логируем историю
#
#     if len(history) > 1:
#         current_state_name = history.pop()  # Удаляем текущее состояние
#         previous_state_name = history[-1]  # Берем **ПОСЛЕДНЕЕ** оставшееся состояние
#         previous_state = getattr(UserState, previous_state_name.split(":")[-1],
#                                  UserState.start_section)  # Конвертируем в State
#     else:
#         previous_state_name = "UserState:start_section"
#         previous_state = UserState.start_section  # Если истории нет, возвращаемся в старт
#
#     await state.update_data(history=history)
#     await state.set_state(previous_state)
#
#     print(f"Переход к состоянию: {previous_state_name}")  # Логируем состояние
#
#     # Обрабатываем возврат на предыдущую страницу в зависимости от состояния
#     if previous_state_name == UserState.start_section:
#         await start_command(callback, state)  # Переводим пользователя в главное меню
#         await callback.answer("Вы вернулись в главное меню.")
#     elif previous_state_name == UserState.catalog_selection:
#         await section_shop(callback, state)  # Возвращаем к выбору категории
#     elif previous_state_name == UserState.product_type_selection:
#         await category_selection(callback, state)
#     elif previous_state_name == UserState.product_selection:
#         await show_products(callback, state)  # Возвращаем к выбору подкатегории
#     elif previous_state_name == UserState.product_details_section:
#         await show_product_details(callback, state)
#
#
#     elif previous_state_name == UserState.basket_section:
#         await show_user_cart(callback, state)  # Возвращаем к корзине
#     elif previous_state_name == UserState.basket_item_select:
#         await show_selected_product(callback, state)  # Возвращаем к выбранному товару

@router.callback_query(F.data == 'back')
async def back_to_previous_state(callback: CallbackQuery, state: FSMContext):
    """Возвращает пользователя к предыдущему состоянию"""
    data = await state.get_data()
    history = data.get("history", [])
    print(f"История состояний перед возвратом: {history}")  # Логируем историю

    if len(history) > 1:
        current_state_name = history.pop()  # Удаляем текущее состояние
        previous_state_name = history[-1]  # Берем **ПОСЛЕДНЕЕ** оставшееся состояние
        previous_state = getattr(UserState, previous_state_name.split(":")[-1],
                                 UserState.start_section)  # Конвертируем в State
    else:
        previous_state_name = "UserState:start_section"
        previous_state = UserState.start_section  # Если истории нет, возвращаемся в старт

    await state.update_data(history=history)
    await state.set_state(previous_state)

    print(f"Переход к состоянию: {previous_state_name}")  # Логируем состояние

    # Обрабатываем возврат на предыдущую страницу в зависимости от состояния
    if previous_state_name == UserState.start_section:
        await start_command(callback, state)  # Переводим пользователя в главное меню
        await callback.answer("Вы вернулись в главное меню.")
    elif previous_state_name == UserState.catalog_selection:
        await section_shop(callback, state)  # Возвращаем к выбору категории
    elif previous_state_name == UserState.product_type_selection:
        # Извлекаем категорию из истории состояний и передаем в category_selection
        history = await state.get_data()
        previous_category = history.get('subcategory', None)
        if previous_category:
            await category_selection(callback, state)  # Возвращаем в выбор категории
        else:
            await section_shop(callback, state)  # Если категории нет, возвращаем в раздел выбора
    elif previous_state_name == UserState.product_selection:
        await show_products(callback, state)  # Возвращаем к выбору подкатегории
    elif previous_state_name == UserState.product_details_section:
        await show_product_details(callback, state)


    elif previous_state_name == UserState.basket_section:
        await show_user_cart(callback, state)  # Возвращаем к корзине
    elif previous_state_name == UserState.basket_item_select:
        await show_selected_product(callback, state)  # Возвращаем к выбранному товару


