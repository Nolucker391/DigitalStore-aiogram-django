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

def apple_builder():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='⌚️Watches', callback_data='AppleWatches'),
        types.InlineKeyboardButton(text='💻Laptops ', callback_data='AppleLaptops')
    )
    builder.row(
        types.InlineKeyboardButton(text='📱Phones', callback_data='IPhones'),
    )
    builder.row(
        types.InlineKeyboardButton(text='<< назад', callback_data='back'),
    )

    return builder

def sony_builder():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='🎮 PlayStation', callback_data='SonyPlaystation'),
        types.InlineKeyboardButton(text='🎧 Headphones', callback_data='SonyHeadphones')
    )
    builder.row(
        types.InlineKeyboardButton(text='<< назад', callback_data='back'),
    )
    return builder

def samsung_builder():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='📺 TVs', callback_data='SamsungTVs')
    )
    builder.row(
        types.InlineKeyboardButton(text='<< назад', callback_data='back'),
    )
    return builder