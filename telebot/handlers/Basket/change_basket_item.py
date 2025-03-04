from aiogram import types, F
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from handlers.routes import router
from basket.models import Basket
from products.models import Product
from keyboards.menu.main_menu import InlineKeyboardBuilder


async def get_basket_item(telegram_id, product_id):
    """ Получает товар из корзины по telegram_id и product_id """
    return await sync_to_async(lambda: Basket.objects.filter(telegram_id=telegram_id, product_id=product_id).first())()


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
    await sync_to_async(Basket.objects.filter(telegram_id=telegram_id, product_id=product_id).delete)()


@router.callback_query(F.data.startswith("select_product_"))
async def show_selected_product(callback: types.CallbackQuery):
    """ Отображает выбранный товар с возможностью изменения количества """
    user_id = callback.from_user.id
    product_id = int(callback.data.split("_")[-1])

    basket_item = await get_basket_item(user_id, product_id)
    if not basket_item:
        await callback.answer("❌ Товар не найден в корзине!")
        return

    product = basket_item.product  # Связанный товар
    caption = f"<b>{product.name}</b>\n💰 Цена: {product.price} руб.\n🛒 Количество: {basket_item.count}"

    keyboard = build_cart_keyboard(product_id, basket_item.count)
    keyboard.row(
        types.InlineKeyboardButton(text="🗑 Удалить товар", callback_data=f"delete_product_{product_id}")
    )

    await callback.message.edit_text(caption, reply_markup=keyboard.as_markup())

