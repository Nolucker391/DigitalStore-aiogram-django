from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def laptop_builder():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='Apple', callback_data='Apple'),
        types.InlineKeyboardButton(text='Huawei', callback_data='Huawei')
    )
    builder.row(
        types.InlineKeyboardButton(text='Lenovo', callback_data='Lenovo'),
    )
    builder.row(
        types.InlineKeyboardButton(text='<< назад', callback_data='back'),
    )

    return builder