from aiogram import F
from aiogram.types import CallbackQuery

from handlers.Catalog.subcategories.computers import computer_selection, show_gaming_pc_with_cart
from handlers.Catalog.subcategories.laptops import laptops_selection
from handlers.Catalog.subcategories.monoblocks import monoblock_selection
from handlers.DefaultCommands.StartCommand import start_command
from handlers.Catalog.categories import section_shop
from handlers.routes import router
from aiogram.fsm.context import FSMContext

from states.states import UserState


@router.callback_query(F.data == 'back')
async def back_to_menu(callback: CallbackQuery,  state: FSMContext):
    data = await state.get_data()
    history = data.get("history", [])
    if len(history) > 1:  # Если есть куда возвращаться
        history.pop()  # Удаляем текущее состояние
        previous_state = history[-1]  # Берем предыдущее состояние
    else:
        previous_state = UserState.start_section  # Если история пуста, возвращаем в главное меню

    await state.update_data(history=history)  # Обновляем историю
    await state.set_state(previous_state)  # Возвращаем предыдущее состояние
        # Определяем, куда вернуть пользователя
    if previous_state == UserState.start_section:
        # await start_command(callback.message, state)
        await start_command(callback, state)  # Передаем callback вместо callback.message
        await callback.answer("Вы вернулись в главное меню.")
    elif previous_state == UserState.first_section:
        await section_shop(callback, state)
    elif previous_state == UserState.select_laptops:
        await laptops_selection(callback, state)
    elif previous_state == UserState.select_monoblocks:
        await monoblock_selection(callback, state)
    elif previous_state == UserState.select_computer:
        await computer_selection(callback, state)
    elif previous_state == UserState.select_gaming_pc:
        await computer_selection(callback, state)




