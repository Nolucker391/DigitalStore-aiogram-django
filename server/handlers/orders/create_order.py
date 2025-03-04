import asyncio
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, PreCheckoutQuery, LabeledPrice
from asgiref.sync import sync_to_async
from config.config_reader import config
from handlers.routes import router, logger
from orders.models import Order
from basket.models import Basket

# 🏦 Получаем платежный токен
provider_token = config.payment_token.get_secret_value()

@router.callback_query(F.data == "accept_order")
async def start_order(callback: types.CallbackQuery, state: FSMContext):
    """Начинает оформление заказа (тестовый платёж)"""
    """Пользователь выбрал оплату товара"""
    try:
        await callback.message.delete()

        prices = [LabeledPrice(label="Тестовый заказ", amount=5000)]  # 50.00 RUB в копейках
        currency = "RUB"

        # ✅ Создаем inline-клавиатуру с кнопкой "Оплатить"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Кассовый чек", pay=True)],
                [InlineKeyboardButton(text="💳 Оплатить", callback_data="pay_order")]
            ]
        )
        # Сохраняем сумму и валюту в state (контекст)
        await state.update_data(amount=prices[0].amount / 100, currency=currency)

        logger.info(f"🛒 Отправка платежа: {prices}, Валюта: {currency}, Провайдер: {provider_token}")

        await callback.bot.send_invoice(
            chat_id=callback.message.chat.id,
            title="Тестовая покупка",
            description="Покупка товара (тест)\n⚠️ Кассовый чек доступен только в мобильном приложении Telegram (Android/iOS).",
            payload="test_payment",
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            start_parameter="test_order_123",
            need_email=False,
            need_phone_number=True,
            reply_markup=keyboard
        )

    except Exception as e:
        logger.error(f"❌ Ошибка при отправке платежа: {e}")
        await callback.message.answer("🚨 Произошла ошибка при создании платежа. Попробуйте еще раз.")


@router.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query: PreCheckoutQuery):
    """Подтверждаем платеж"""
    await pre_checkout_query.answer(ok=True)


@router.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message, state: FSMContext):
    """Обрабатывает успешный платеж"""
    # просто реализация уже исходя из реальной оплаты
    pass


@sync_to_async
def delete_basket(telegram_id):
    """Асинхронное удаление товаров из корзины"""
    Basket.objects.filter(telegram_id=telegram_id).delete()

@sync_to_async
def create_order(telegram_id, full_name):
    """Асинхронное создание заказа"""
    return Order.objects.create(
        telegram_id=telegram_id,
        full_name=full_name,
        status="Оплачен"
    )

@router.callback_query(F.data == "pay_order")
async def procces_success_orderpay(callback: types.CallbackQuery, state: FSMContext):
    """Процесс обработки заказа и добавления в БД."""
    logger.info(f"Пользователь {callback.from_user.first_name} успешно оплатил корзину.")
    await callback.message.delete()

    user_data = await state.get_data()
    telegram_id = callback.from_user.id
    full_name = callback.from_user.full_name

    await delete_basket(telegram_id)  # ✅ Удаляем товары из корзины
    order = await create_order(telegram_id, full_name)  # ✅ Создаем заказ в БД

    amount = user_data.get("amount", "Неизвестно")
    currency = user_data.get("currency", "Неизвестно")
    logger.info(f"🛒 Новый заказ #{order.id} от {full_name} ({telegram_id}) на сумму {amount} {currency}")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="back_to_menu")]
        ]
    )

    await callback.message.answer(
        f"✅ <b>Оплата прошла успешно!</b>\n\n"
        f"💰 Сумма: {amount} {currency}\n"
        f"📌 Заказ оформлен!",
        reply_markup=keyboard
    )

from handlers.DefaultCommands.StartCommand import start_command

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    """Обрабатывает кнопку '🔙 Вернуться в меню'"""
    await callback.message.delete()
    await start_command(callback, state)
