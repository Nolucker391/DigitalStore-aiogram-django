from aiogram import types, F
from aiogram.types import InputMediaPhoto, FSInputFile
from asgiref.sync import sync_to_async

from handlers.routes import router
from aiogram.fsm.context import FSMContext

from basket.models import Basket
from products.models import Product
from keyboards.menu.main_menu import InlineKeyboardBuilder


async def get_user_basket(telegram_id):
    """Получает список товаров в корзине пользователя по его Telegram ID с загруженными продуктами"""
    return await sync_to_async(
        lambda: list(Basket.objects.select_related("product").filter(telegram_id=telegram_id))
    )()


@router.callback_query(F.data == 'second_block')
async def show_user_cart(callback: types.CallbackQuery, state: FSMContext):
    """ Отображает корзину пользователя с выбранными товарами """
    user_id = callback.from_user.id

    basket_items = await get_user_basket(user_id)  # Получаем товары из корзины

    if not basket_items:
        await callback.message.answer("🛒 Ваша корзина пуста!")
        return

    # Создаём описание корзины
    description = "🛍 <b>Ваши выбранные продукты:</b>\n\n"
    total_price = sum(item.total_price for item in basket_items)  # Считаем общую сумму
    buttons = []

    for idx, item in enumerate(basket_items, 1):
        product_name = item.product.name  # Теперь product уже загружен
        description += f"{idx}. <b>{product_name}</b> — {item.count} шт. — {item.total_price} руб.\n"

        # Добавляем кнопку для выбора товара
        buttons.append(types.InlineKeyboardButton(
            text=f"{idx} - Изменить {product_name}", callback_data=f"select_product_{item.product.id}"
        ))


    description += f"\n<b>Итого:</b> {total_price} руб."

    # Указываем твой статичный файл для фото (измените путь)
    file_path = "bot/assets/images/computers.png"

    # Создаём клавиатуру
    builder = InlineKeyboardBuilder()
    for btn in buttons:
        builder.row(btn)
    builder.row(
        types.InlineKeyboardButton(text="🔙 Вернуться", callback_data="back"),
        types.InlineKeyboardButton(text="📋 Оформить заказ", callback_data="accept_order")
    )

    # Обновляем сообщение (используем статичное изображение)
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(file_path),
            caption=description
        ),
        reply_markup=builder.as_markup()
    )
