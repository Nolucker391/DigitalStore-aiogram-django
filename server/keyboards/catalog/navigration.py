from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder



def build_navigation_keyboard(index: int, total: int, product_id: int):
    """ Создает клавиатуру с кнопками навигации по товарам """
    builder = InlineKeyboardBuilder()

    # Кнопки навигации
    row = []
    if index > 0:
        row.append(types.InlineKeyboardButton(text="⬅️ Предыдущая", callback_data="prev_product"))
    row.append(types.InlineKeyboardButton(text="🛒 В корзину", callback_data=f"add_basket_{product_id}"))
    if index < total - 1:
        row.append(types.InlineKeyboardButton(text="Cледующая ➡", callback_data="next_product"))

    builder.row(*row)
    builder.row(types.InlineKeyboardButton(text="🔙 Вернуться", callback_data="back"))

    return builder


def build_cart_keyboard(product_id: int, count: int):
    """ Создает клавиатуру с кнопками изменения количества и удаления товара """
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text='➖', callback_data=f'decrease_{product_id}'),
        types.InlineKeyboardButton(text=f'{count}', callback_data='ignore'),  # Просто показывает кол-во
        types.InlineKeyboardButton(text='➕', callback_data=f'increase_{product_id}')
    )
    builder.row(
        types.InlineKeyboardButton(text='<< Назад', callback_data='back'),
    )

    return builder

