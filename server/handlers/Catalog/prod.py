from aiogram import types, F
from aiogram.types import InputMediaPhoto, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers.routes import router, logger
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from products.models import Product, Category

from states.history_static import set_user_state
from states.states import UserState


@router.callback_query(F.data.regexp(r'^product_(\d+)$'))
async def show_product_details(callback: types.CallbackQuery, state: FSMContext):
    """ Обработчик для показа деталей продукта """
    await set_user_state(state, UserState.product_details_section)

    product_id = callback.data.split('_')[1]  # Извлекаем product_id из callback_data
    product = await sync_to_async(lambda: Product.objects.filter(id=product_id).first())()

    if not product:
        await callback.answer("❌ Продукт не найден.")
        return

    images = await sync_to_async(lambda: list(product.images.all()))()
    image_paths = [image.image.path for image in images] if images else ["server/assets/images/computers.png"]

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🛒 В корзину", callback_data=f"add_basket_{product.id}"))
    builder.row(types.InlineKeyboardButton(text="<< Назад", callback_data="back"))


    await callback.message.delete()

    await callback.message.answer_photo(
        FSInputFile(image_paths[0]),
        caption=f"🖥 <b>Название:</b> {product.name}\n📜 <b>Описание:</b>\n {product.description}\n💰 <b>Цена:</b> {product.price} руб.",
        reply_markup=builder.as_markup()
    )

    # media_group = [InputMediaPhoto(media=FSInputFile(image_path), caption=f"🖥 <b>Название:</b> {product.name}\n📜 <b>Описание:</b>\n {product.description}\n💰 <b>Цена:</b> {product.price} руб.") for image_path in image_paths]
    # await callback.message.answer_media_group(media=media_group)
    # await callback.message.answer(text="", reply_markup=builder.as_markup())