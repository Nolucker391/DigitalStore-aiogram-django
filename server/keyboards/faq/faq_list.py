from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def faq_list_questins():
    builder_inline = InlineKeyboardBuilder()

    builder_inline.row(
        types.InlineKeyboardButton(text='Оплатил заказа, что делать дальше?', callback_data='first'),
    )
    builder_inline.row(
        types.InlineKeyboardButton(text='Собрал кучу товаров в корзину, не дает оформить.', callback_data='second'),
    )
    builder_inline.row(
        types.InlineKeyboardButton(text='Заказал ваш продукт, товар не соотвествует описанию.', callback_data="third")
    )
    builder_inline.row(
        types.InlineKeyboardButton(text='Как дела?', callback_data="fourth")
    )
    builder_inline.row(
        types.InlineKeyboardButton(text='🔙Вернуться', callback_data="back"),
        types.InlineKeyboardButton(text='Задать свой вопрос', callback_data="five")
    )
    return builder_inline


