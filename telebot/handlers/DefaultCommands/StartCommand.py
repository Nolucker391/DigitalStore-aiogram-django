# from aiogram import types
# from aiogram.types import Message, FSInputFile, InputMediaPhoto
# from aiogram.filters import CommandStart, Command
# from asgiref.sync import sync_to_async
# from keyboards.menu.main_menu import key_start
# from handlers.routes import router
# from aiogram.fsm.context import FSMContext
#
# from states.states import UserState
# from states.history_static import set_user_state
#
# from users.models import User
# from django.db.utils import IntegrityError
# from bot import bot
#
# channel_id = -1002270090309
# async def check_subscription(user_id: int) -> bool:
#     try:
#         chat_member_channel = await bot.get_chat_member(channel_id, user_id)
#         return chat_member_channel.status in ["member", "administrator", "creator"]
#     except Exception as e:
#         print(f"Ошибка проверки подписки: {e}")
#         return False
#
# # Функция для добавления пользователя в БД (СИНХРОННАЯ)
# def add_user(tg_id, username, first_name):
#     try:
#         user, created = User.objects.get_or_create(
#             tg_id=tg_id,
#             defaults={"username": username, "first_name": first_name}
#         )
#         return user, created
#     except IntegrityError:
#         return None, False
#
#
# @router.message(CommandStart())
# async def start_command(message_or_callback: types.Message | types.CallbackQuery, state: FSMContext):
#     await state.update_data(history=[])
#     await set_user_state(state, UserState.start_section)
#
#     # Определяем user_id в зависимости от типа запроса
#     if isinstance(message_or_callback, types.CallbackQuery):
#         user_id = message_or_callback.from_user.id
#         message = message_or_callback.message  # Берем сообщение из callback
#     else:
#         user_id = message_or_callback.from_user.id
#         message = message_or_callback
#
#     is_subscribed = await check_subscription(user_id)
#     if not is_subscribed:
#         await message.answer("❌ Вы не подписаны на канал. Для продолжения подпишитесь. \nСсылка: https://t.me/+P_CQEATSreExZDc6")
#         return
#
#     builder_menu = key_start()
#     file_path = "bot/assets/images/menu.png"
#
#     # Добавляем пользователя в БД
#     print(f"ID пользователя: {user_id}")
#     user, created = await sync_to_async(add_user)(user_id, message.from_user.username, message.from_user.first_name)
#
#     if user:
#         if created:
#             print(f"✅ Новый пользователь зарегистрирован: {user}")
#         else:
#             print(f"ℹ️ Пользователь уже существует: {user}")
#     else:
#         print(f"❌ Ошибка при добавлении пользователя {user_id}")
#
#     try:
#         await message.edit_media(
#             media=InputMediaPhoto(
#                 media=FSInputFile(file_path),
#                 caption="Привет 👋, Я - <b>БОТ</b>ан.🤖\n"
#                         "\n<b>Вы</b> - 💁‍♂️можете просматривать доступные товары, заполнять корзину и самое главное - приобрести интересующий <b>Вам</b> - продукт.⤵️️",
#             ),
#             reply_markup=builder_menu.as_markup()
#         )
#     except Exception:
#         await message.answer_photo(
#             photo=FSInputFile(file_path),
#             caption="Привет 👋, Я - <b>БОТ</b>ан.🤖\n"
#                     "\n<b>Вы</b> - 💁‍♂️можете просматривать доступные товары, заполнять корзину и самое главное - приобрести интересующий <b>Вам</b> - продукт.⤵️️",
#             reply_markup=builder_menu.as_markup()
#         )
#
#
#
# @router.message(Command("history"))
# async def show_history(message: Message, state: FSMContext):
#     data = await state.get_data()
#     history = data.get("history", [])  # Получаем историю состояний
#
#     print(history)
from aiogram import types
from aiogram.types import Message, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart, Command
from asgiref.sync import sync_to_async
from keyboards.menu.main_menu import key_start
from handlers.routes import router
from aiogram.fsm.context import FSMContext

from states.states import UserState
from states.history_static import set_user_state

from users.models import User
from django.db.utils import IntegrityError
from bot import bot

channel_id = -1002270090309

async def check_subscription(user_id: int) -> bool:
    try:
        chat_member_channel = await bot.get_chat_member(channel_id, user_id)
        return chat_member_channel.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False

# Функция для добавления пользователя в БД (СИНХРОННАЯ)
def add_user(tg_id, username, first_name):
    try:
        user, created = User.objects.get_or_create(
            tg_id=tg_id,
            defaults={"username": username or "", "first_name": first_name or ""}
        )
        return user, created
    except IntegrityError:
        return None, False

@router.message(CommandStart())
async def start_command(message_or_callback: types.Message | types.CallbackQuery, state: FSMContext):
    await state.update_data(history=[])
    await set_user_state(state, UserState.start_section)

    # Определяем user_id в зависимости от типа запроса
    if isinstance(message_or_callback, types.CallbackQuery):
        user = message_or_callback.from_user
        message = message_or_callback.message  # Берем сообщение из callback
    else:
        user = message_or_callback.from_user
        message = message_or_callback

    user_id = user.id
    username = user.username
    first_name = user.first_name

    print(f"🔍 Данные пользователя: ID: {user_id}, Username: {username}, First Name: {first_name}")

    is_subscribed = await check_subscription(user_id)
    if not is_subscribed:
        await message.answer("❌ Вы не подписаны на канал. Для продолжения подпишитесь. \nСсылка: https://t.me/+P_CQEATSreExZDc6")
        return

    builder_menu = key_start()
    file_path = "bot/assets/images/menu.png"

    # Добавляем пользователя в БД
    user_db, created = await sync_to_async(add_user)(user_id, username, first_name)

    if user_db:
        if created:
            print(f"✅ Новый пользователь зарегистрирован: {user_db}")
        else:
            print(f"ℹ️ Пользователь уже существует: {user_db}")
    else:
        print(f"❌ Ошибка при добавлении пользователя {user_id}")

    try:
        await message.edit_media(
            media=InputMediaPhoto(
                media=FSInputFile(file_path),
                caption="Привет 👋, Я - <b>БОТ</b>ан.🤖\n"
                        "\n<b>Вы</b> - 💁‍♂️можете просматривать доступные товары, заполнять корзину и самое главное - приобрести интересующий <b>Вам</b> - продукт.⤵️️",
            ),
            reply_markup=builder_menu.as_markup()
        )
    except Exception:
        await message.answer_photo(
            photo=FSInputFile(file_path),
            caption="Привет 👋, Я - <b>БОТ</b>ан.🤖\n"
                    "\n<b>Вы</b> - 💁‍♂️можете просматривать доступные товары, заполнять корзину и самое главное - приобрести интересующий <b>Вам</b> - продукт.⤵️️",
            reply_markup=builder_menu.as_markup()
        )

@router.message(Command("history"))
async def show_history(message: Message, state: FSMContext):
    data = await state.get_data()
    history = data.get("history", [])  # Получаем историю состояний

    print(history)
