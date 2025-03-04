from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext


async def set_user_state(state: FSMContext, new_state: State):
    """Сохраняем новое состояние и обновляем историю"""
    data = await state.get_data()
    history = data.get("history", [])

    # Добавляем в историю только если его там нет (чтобы избежать дублирования)
    if not history or history[-1] != new_state.state:
        history.append(new_state.state)

    await state.update_data(history=history)  # Обновляем стек истории
    await state.set_state(new_state)  # Устанавливаем текущее состояние
