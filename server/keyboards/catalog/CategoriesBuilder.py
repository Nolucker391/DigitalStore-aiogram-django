from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
    
def cat_builder():
    builder_for_first_button = InlineKeyboardBuilder()
    builder_for_first_button.row(
        types.InlineKeyboardButton(text='🍏 Apple ', callback_data='AppleCat'),
        types.InlineKeyboardButton(text='👾 Sony', callback_data='SonyCat')
    )
    builder_for_first_button.row(
        types.InlineKeyboardButton(text='🕋 Samsung', callback_data='SamsungCat')
    )
    builder_for_first_button.row(
        types.InlineKeyboardButton(text='<< назад', callback_data='back'),
    )

    return builder_for_first_button