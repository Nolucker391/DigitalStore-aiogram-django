from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    start_section = State()
    first_section = State()
    select_computer = State()
    select_laptops = State()
    select_monoblocks = State()

    select_gaming_pc = State()

    add_basket_prod = State()

    basket_section = State()
    basket_item_select = State()

    OrderState = State()

class OrderState(StatesGroup):
    waiting_for_name = State()
    waiting_for_address = State()
    waiting_for_phone = State()
    waiting_for_payment = State()

