from aiogram import types, F
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from handlers.routes import router, logger
from basket.models import Basket
from products.models import Product
from aiogram.utils.keyboard import InlineKeyboardBuilder
from states.history_static import set_user_state
from states.states import UserState

async def get_basket_item(telegram_id, product_id):
    """ Получает товар из корзины по telegram_id и product_id """
    return await sync_to_async(lambda: Basket.objects.select_related("product").filter(
        telegram_id=telegram_id, product_id=product_id
    ).first())()

async def update_basket_item(telegram_id, product_id, count_change):
    """ Обновляет количество товара в корзине """
    basket_item = await get_basket_item(telegram_id, product_id)
    if basket_item:
        new_count = basket_item.count + count_change
        if new_count <= 0:
            await delete_basket_item(telegram_id, product_id)  # Удаляем, если 0
            return None
        basket_item.count = new_count
        await sync_to_async(basket_item.save)()
    return basket_item

async def delete_basket_item(telegram_id, product_id):
    """ Удаляет товар из корзины """
    await sync_to_async(lambda: Basket.objects.filter(telegram_id=telegram_id, product_id=product_id).delete())()



from aiogram.types import InputMediaPhoto, FSInputFile
from keyboards.catalog.navigration import build_cart_keyboard

@router.callback_query(F.data.startswith("select_product_"))
async def show_selected_product(callback: types.CallbackQuery, state: FSMContext):
    """ Отображает выбранный товар с возможностью изменения количества """
    await set_user_state(state, UserState.basket_item_select)

    user_id = callback.from_user.id
    product_id = int(callback.data.split("_")[-1])

    basket_item = await get_basket_item(user_id, product_id)
    if not basket_item:
        await callback.answer("❌ Товар не найден в корзине!")
        return

    product = basket_item.product
    caption = f"<b>{product.name}</b>\n💰 Цена: {product.price} руб.\n🛒 Количество: {basket_item.count}"
    keyboard = build_cart_keyboard(product_id, basket_item.count)

    buttons = keyboard.export()

    # Удаляем кнопку "Назад"
    for row in buttons:
        row[:] = [btn for btn in row if btn.callback_data != "back"]

    # Создаём новую клавиатуру и добавляем оставшиеся кнопки
    keyboard = InlineKeyboardBuilder()
    for row in buttons:
        keyboard.row(*row)

    # Добавляем новые кнопки
    keyboard.row(
        types.InlineKeyboardButton(text="🗑 Удалить товар", callback_data=f"delete_product_{product_id}"),
        types.InlineKeyboardButton(text="🔙 Назад", callback_data="back")
    )
    images = await sync_to_async(lambda: list(product.images.all()))()
    image_path = images[0].image.path if images else "server/assets/images/computers.png"
    try:
        if callback.message.photo:
            await callback.message.edit_media(
                media=InputMediaPhoto(
                    media=FSInputFile(image_path),
                    caption=caption
                ),
                reply_markup=keyboard.as_markup()
            )
        else:
            await callback.message.edit_text(caption, reply_markup=keyboard.as_markup())
    except Exception as e:
        await callback.answer("⚠️ Ошибка: нельзя изменить сообщение!", show_alert=True)


@router.callback_query(F.data.startswith("increase_"))
async def increase_product(callback: types.CallbackQuery):
    """ Увеличивает количество товара в корзине """
    logger.info(f"Пользователь: {callback.from_user.first_name} увеличил кол-во продукта в корзине.")

    user_id = callback.from_user.id
    product_id = int(callback.data.split("_")[-1])

    basket_item = await update_basket_item(user_id, product_id, 1)
    if not basket_item:
        await callback.answer("❌ Ошибка при обновлении количества!")
        return

    await show_selected_product(callback)

@router.callback_query(F.data.startswith("decrease_"))
async def decrease_product(callback: types.CallbackQuery):
    """ Уменьшает количество товара в корзине """
    logger.info(f"Пользователь: {callback.from_user.first_name} уменьшил кол-во продукта в корзине.")

    user_id = callback.from_user.id
    product_id = int(callback.data.split("_")[-1])

    basket_item = await update_basket_item(user_id, product_id, -1)
    if not basket_item:
        await callback.message.delete()  # Удаляем сообщение, если товара нет
        return

    await show_selected_product(callback)

from handlers.DefaultCommands.StartCommand import start_command

@router.callback_query(F.data.startswith("delete_product_"))
async def delete_product(callback: types.CallbackQuery, state: FSMContext):
    """ Удаляет товар из корзины """
    logger.info(f"Пользователь: {callback.from_user.first_name} удалил продукт с корзины.")

    user_id = callback.from_user.id
    product_id = int(callback.data.split("_")[-1])

    await delete_basket_item(user_id, product_id)
    await callback.answer("Вы удалили продукт с корзины!")
    # await callback.message.delete()  # Удаляем сообщение, так как товара больше нет
    await start_command(callback, state)  # Передаем callback вместо callback.message