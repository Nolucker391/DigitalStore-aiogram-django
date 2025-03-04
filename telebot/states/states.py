from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    start_section = State()
    first_section = State()
    select_computer = State()
    select_laptops = State()
    select_monoblocks = State()

    select_gaming_pc = State()

    add_basket_prod = State()


