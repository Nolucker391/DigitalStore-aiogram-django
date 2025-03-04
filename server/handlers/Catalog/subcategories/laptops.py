from aiogram import types, F
from aiogram.types import InputMediaPhoto, FSInputFile

from states.history_static import set_user_state
from handlers.routes import router
from aiogram.fsm.context import FSMContext
from states.states import UserState
from keyboards.catalog.sub_cat.LaptopsBuilder import laptop_builder


from aiogram import types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto, FSInputFile
from asgiref.sync import sync_to_async

from handlers.routes import router, logger
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


@router.callback_query(F.data == 'laptops')
async def laptops_selection(callback: types.CallbackQuery, state: FSMContext):
    builder = laptop_builder()
    file_path = "server/assets/images/laptops.png"

    logger.info(f"Пользователь: {callback.from_user.first_name} выбрал раздел Ноутбуков.")

    try:
        await set_user_state(state, UserState.select_laptops)
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=FSInputFile(file_path),  # Новый путь к фото
                caption="Выберите интересующую модель.🪬"
            ),
            reply_markup=builder.as_markup()  # Обновленные кнопки (если нужны)
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return
        else:
            raise

