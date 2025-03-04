from aiogram import types, F
from aiogram.types import InputMediaPhoto, FSInputFile
from asgiref.sync import sync_to_async

from handlers.routes import router
from aiogram.fsm.context import FSMContext

from states.history_static import set_user_state
from states.states import UserState
from keyboards.catalog.sub_cat.ComputersBuilder import computer_builder, build_navigation_keyboard
from products.models import Product, Category


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


@router.callback_query(F.data == 'computers')
async def computer_selection(callback: types.CallbackQuery, state: FSMContext):
    """ Выбор категории 'Компьютеры' """
    builder = computer_builder()
    file_path = "bot/assets/images/computers.png"

    await set_user_state(state, UserState.select_computer)
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(file_path),
            caption="Выберите интересующую подкатегорию 🖥"
        ),
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == 'gaming')
async def show_gaming_pc_with_cart(callback: types.CallbackQuery, state: FSMContext):
    """ Показывает товары из подкатегории 'Игровые компьютеры', если она принадлежит категории 'Компьютеры' """
    await set_user_state(state, UserState.select_gaming_pc)

    products = await get_subcategory_products("компьютеры", "игровые")  # Получаем товары

    if not products:
        await callback.answer("❌ В подкатегории 'Игровые компьютеры' пока нет товаров.")
        return

    # Записываем список товаров и текущий индекс в FSMContext
    await state.update_data(products=products, product_index=0)

    await update_product_message(callback, state)  # Вызываем функцию обновления сообщения


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
    image_path = images[0].image.path if images else "bot/assets/images/default.png"

    builder = build_navigation_keyboard(index, len(products), prod.id)  # Создаем клавиатуру

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(image_path),
            caption=f"🖥 <b>Название:</b> {prod.name}\n📜 <b>Описание:</b> {prod.description}\n💰 <b>Цена:</b> {prod.price} руб."
        ),
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.in_(["prev_product", "next_product"]))
async def change_product(callback: types.CallbackQuery, state: FSMContext):
    """ Листает товары вперёд и назад """
    data = await state.get_data()
    index = data.get("product_index", 0)
    products = data.get("products", [])

    if callback.data == "next_product" and index < len(products) - 1:
        index += 1
    elif callback.data == "prev_product" and index > 0:
        index -= 1

    await state.update_data(product_index=index)  # Обновляем индекс товара
    await update_product_message(callback, state)  # Обновляем сообщение