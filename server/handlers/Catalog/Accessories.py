from aiogram import types, F
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers.routes import router, logger
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from products.models import Product, Category

from states.history_static import set_user_state
from states.states import UserState

async def get_subcategory_products(parent_category_name, subcategory_name):
    """ Получает список товаров из категории и подкатегории Django ORM """
    parent_category = await sync_to_async(lambda: Category.objects.filter(name=parent_category_name).first())()
    if not parent_category:
        return []
    subcategory = await sync_to_async(lambda: parent_category.subcategories.filter(name=subcategory_name).first())()
    if not subcategory:
        return []
    products = await sync_to_async(lambda: list(subcategory.products.all()))()
    return products


@router.callback_query(F.data.in_({'AppleWatches', 'AppleLaptops', 'IPhones', 'SonyPlaystation', 'SonyHeadphones', 'SamsungTVs'}))
async def show_products(callback: types.CallbackQuery, state: FSMContext):
    """ Показывает первую страницу товаров """
    subcategory_map = {
        'AppleWatches': ('Apple', 'Watches', 'server/assets/images/botPC.png'),
        'AppleLaptops': ('Apple', 'Laptops', 'server/assets/images/botPC.png'),
        'IPhones': ('Apple', 'Phones', 'server/assets/images/botPC.png'),
        'SonyPlaystation': ('Sony', 'PlayStation', 'server/assets/images/botPC.png'),
        'SonyHeadphones': ('Sony', 'Headphones', 'server/assets/images/botPC.png'),
        'SamsungTVs': ('Samsung', 'TVs', 'server/assets/images/botPC.png'),
    }
    print(callback.data)
    category, subcategory, file_path = subcategory_map[callback.data]

    data = await state.get_data()
    history = data.get("history", [])
    history.append(f"subcategory_selection:{callback.data}")
    await state.update_data(history=history)

    await set_user_state(state, UserState.product_selection)
    await send_product_list(callback, callback.data, category, subcategory, file_path, page=0)

@router.callback_query(F.data.regexp(r'^(AppleWatches|AppleLaptops|IPhones)_\d+$'))
async def paginate_products(callback: types.CallbackQuery, state: FSMContext):
    """ Обработчик для переключения страниц товаров """
    subcategory_map = {
        'AppleWatches': ('Apple', 'Watches', 'server/assets/images/botPC.png'),
        'AppleLaptops': ('Apple', 'Laptops', 'server/assets/images/botPC.png'),
        'IPhones': ('Apple', 'Phones', 'server/assets/images/botPC.png'),
        'SonyPlaystation': ('Sony', 'PlayStation', 'server/assets/images/botPC.png'),
        'SonyHeadphones': ('Sony', 'Headphones', 'server/assets/images/botPC.png'),
        'SamsungTVs': ('Samsung', 'TVs', 'server/assets/images/botPC.png'),
    }

    callback_data_parts = callback.data.split('_')
    subcategory_key = callback_data_parts[0]  # AppleWatches, AppleLaptops, IPhones
    page = int(callback_data_parts[1])

    category, subcategory, file_path = subcategory_map[subcategory_key]
    await state.update_data(page=page)

    await send_product_list(callback, subcategory_key, category, subcategory, file_path, page)


async def send_product_list(callback: types.CallbackQuery, subcategory_key: str, category: str, subcategory: str, file_path: str, page: int):
    """ Функция для отправки списка товаров с пагинацией """
    print(category)
    products = await get_subcategory_products(category, subcategory)

    if not products:
        await callback.answer(f'❌ В подкатегории {subcategory} пока нет товаров.')
        return

    items_per_page = 3
    start_index = page * items_per_page
    end_index = start_index + items_per_page
    paginated_products = products[start_index:end_index]

    builder = InlineKeyboardBuilder()

    for product in paginated_products:
        builder.row(types.InlineKeyboardButton(text=f'🛒 {product.name} - {product.price} ₽',
                                               callback_data=f'product_{product.id}'))

    # Кнопки "⬅️ Предыдущая страница" и "➡️ Следующая страница" в одной строке
    navigation_buttons = []
    if page > 0:
        prev_page = f"{subcategory_key}_{page - 1}"
        navigation_buttons.append(types.InlineKeyboardButton(text='⬅️ Предыдущая страница', callback_data=prev_page))
        logger.info(f"Кнопка предыдущая страница: {prev_page}")  # Логируем

    if end_index < len(products):
        next_page = f"{subcategory_key}_{page + 1}"
        navigation_buttons.append(types.InlineKeyboardButton(text='➡️ Следующая страница', callback_data=next_page))
        logger.info(f"Кнопка следующая страница: {next_page}")  # Логируем

    if navigation_buttons:
        builder.row(*navigation_buttons)  # Добавляем обе кнопки в один ряд

    builder.row(types.InlineKeyboardButton(text='<< назад', callback_data="back"))

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(file_path),
            caption=f'📋 Доступные товары ({subcategory}):'
        ),
        reply_markup=builder.as_markup()
    )
