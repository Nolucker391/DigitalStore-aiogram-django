from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def monoblock_bluider():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='Apple', callback_data='Apple'),
        types.InlineKeyboardButton(text='Windows', callback_data='Windows')
    )
    builder.row(
        types.InlineKeyboardButton(text='<< назад', callback_data='back'),
    )

    return builder