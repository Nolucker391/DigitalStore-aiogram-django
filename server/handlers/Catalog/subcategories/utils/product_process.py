from aiogram.types import InputMediaPhoto, FSInputFile
from asgiref.sync import sync_to_async
from keyboards.catalog.sub_cat.ComputersBuilder import computer_builder, build_navigation_keyboard
from products.models import Product, Category

from aiogram import types
from aiogram.fsm.context import FSMContext

async def get_subcategory_products(parent_category_name, subcategory_name):
    """
    Получает товары из подкатегории, если она действительно относится к указанной категории.
    """
    parent_category = await sync_to_async(lambda: Category.objects.filter(name=parent_category_name).first())()
    if not parent_category:
        return []

    # Проверяем, есть ли у родительской категории подкатегория с нужным названием
    subcategory = await sync_to_async(lambda: parent_category.subcategories.filter(name=subcategory_name).first())()

    if not subcategory:
        return []

    # Получаем все товары из этой подкатегории
    products = await sync_to_async(lambda: list(subcategory.products.all()))()
    return products

async def update_product_message(callback: types.CallbackQuery, state: FSMContext):
    """ Обновляет сообщение с информацией о текущем товаре """
    data = await state.get_data()
    products = data.get("products", [])
    index = data.get("product_index", 0)

    if not products:
        await callback.answer("❌ Ошибка: товары не найдены.")
        return

    prod = products[index]  # Берем текущий товар
    images = await sync_to_async(lambda: list(prod.images.all()))()
    image_path = images[0].image.path if images else "server/assets/images/computers.png"
    builder = build_navigation_keyboard(index, len(products), prod.id)  # Создаем клавиатуру

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(image_path),
            caption=f"🖥 <b>Название:</b> {prod.name}\n📜 <b>Описание:</b> {prod.description}\n💰 <b>Цена:</b> {prod.price} руб."
        ),
        reply_markup=builder.as_markup()
    )