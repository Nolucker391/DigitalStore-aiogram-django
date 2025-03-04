from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def cat_builder():
    builder_for_first_button = InlineKeyboardBuilder()
    builder_for_first_button.row(
        types.InlineKeyboardButton(text='💻Ноутбуки', callback_data='laptops'),
        types.InlineKeyboardButton(text='🖥️Моноблоки', callback_data='monoblocks')
    )
    builder_for_first_button.row(
        types.InlineKeyboardButton(text='💾Компьютеры', callback_data='computers')
    )
    builder_for_first_button.row(
        types.InlineKeyboardButton(text='<< назад', callback_data='back'),
    )

    return builder_for_first_button