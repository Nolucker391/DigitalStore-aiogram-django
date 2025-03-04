from aiogram import types, F
from asgiref.sync import sync_to_async
from aiogram.fsm.context import FSMContext
from products.models import Product
# from basket.models import Basket
from handlers.routes import router
from basket.models import Basket
from keyboards.catalog.sub_cat.ComputersBuilder import build_cart_keyboard
# from states.states import UserState
# from states.history_static import set_user_state
from aiogram.fsm.context import FSMContext


@router.callback_query(F.data.startswith('add_basket_'))
async def add_to_cart(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    product_id = int(callback.data.split('_')[-1])
    print(product_id)
    # Проверяем, есть ли товар в корзине
    basket_item, created = await sync_to_async(
        Basket.objects.get_or_create,
    )(telegram_id=user_id, product_id=product_id, defaults={"count": 1})

    if not created:
        basket_item.count += 1
        await sync_to_async(basket_item.save)()

    # Обновляем клавиатуру с количеством товара
    new_keyboard = build_cart_keyboard(product_id, basket_item.count)

    await callback.message.edit_reply_markup(reply_markup=new_keyboard.as_markup())
    await callback.answer(f"Добавлено в корзину! Количество: {basket_item.count}")


@router.callback_query(F.data.startswith('increase_'))
async def increase_quantity(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    product_id = int(callback.data.split('_')[-1])

    basket_item = await sync_to_async(Basket.objects.get)(telegram_id=user_id, product_id=product_id)
    basket_item.count += 1
    await sync_to_async(basket_item.save)()

    new_keyboard = build_cart_keyboard(product_id, basket_item.count)
    await callback.message.edit_reply_markup(reply_markup=new_keyboard.as_markup())
    await callback.answer(f"Количество увеличено: {basket_item.count}")


@router.callback_query(F.data.startswith('decrease_'))
async def decrease_quantity(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    product_id = int(callback.data.split('_')[-1])

    basket_item = await sync_to_async(Basket.objects.get)(telegram_id=user_id, product_id=product_id)

    if basket_item.count > 1:
        basket_item.count -= 1
        await sync_to_async(basket_item.save)()
    else:
        await sync_to_async(basket_item.delete)()  # Удаляем, если 0

    new_count = max(basket_item.count, 1)  # Не показываем 0
    new_keyboard = build_cart_keyboard(product_id, new_count)
    await callback.message.edit_reply_markup(reply_markup=new_keyboard.as_markup())
    await callback.answer(f"Количество уменьшено: {new_count}")
