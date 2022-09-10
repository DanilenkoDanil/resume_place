import time
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from django.conf import settings
from ugc.models import BotMessage, BotButton, Profile
import secrets
import asyncio
import datetime
import json
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


def get_button(button_id: int):
    return BotButton.objects.filter(number=button_id)[0]


def get_service_info(service: str, type_order: str):
    return Service.objects.filter(platform=service, type=type_order)[0]


def get_message(button: BotButton):
    return BotMessage.objects.filter(button=button)[0]


def get_profile(telegram_id: int):
    return Profile.objects.filter(external_id=telegram_id)[0]


def get_active_orders(profile: Profile):
    return Orders.objects.filter(user=profile, status='В работе')


def get_archive_orders(profile: Profile):
    return Orders.objects.filter(user=profile)


def save_message(func):
    async def wrapper(*args, **kwargs):
        message = args[0]
        p, _ = Profile.objects.get_or_create(
            external_id=message.from_user.id,
            defaults={
                'name': message.from_user.username,
                'status': 1
            }
        )
        UsersMessage(
            profile=p,
            text=message.text
        ).save()
        print(kwargs)
        await func(*args, **kwargs)
    return wrapper


def check_button(func):
    async def wrapper(*args, **kwargs):
        print(kwargs)
        await func(*args, **kwargs)
    return wrapper


def create_keyboard(list_id: list):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for button_id in list_id:
        button_request = get_button(button_id)
        if button_request.status is True:
            button = KeyboardButton(button_request.text)
            kb.add(button)
    return kb


token = settings.TOKEN

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

start_kb = create_keyboard([11, 12, 13, 14])
orders_kb = create_keyboard([121, 122, 500])
personal_area_kb = create_keyboard([131, 132, 500])
service_kb = create_keyboard([112, 113, 114, 500])
vk = create_keyboard([1131, 1132, 500])
tik_tok = create_keyboard([1141, 500])
instagram = create_keyboard([1121, 1122, 1123, 500])


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


help_button = get_button(14)
account_button = get_button(13)
promotion_button = get_button(11)
back_button = get_button(500)
add_balance = get_button(131)
ref_button = get_button(132)

orders_button = get_button(12)
orders_active_button = get_button(121)
orders_archive_button = get_button(122)

instagram_button = get_button(112)
instagram_sub_button = get_button(1121)
instagram_story_button = get_button(1122)
instagram_like_button = get_button(1123)

tik_tok_button = get_button(114)
tik_tok_sub_button = get_button(1141)

vk_button = get_button(113)
vk_sub_button = get_button(1131)
vk_like_button = get_button(1132)


# States
class Form(StatesGroup):
    input_amount_service = State()
    input_amount_add_balance = State()
    input_link = State()
    check = State()


@dp.message_handler(commands=['start'], state="*")
@save_message
async def start_message(message: types.Message, state: FSMContext, **kwargs):
    button = get_button(0)
    message_text = get_message(button).text
    await state.finish()
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=start_kb)


# Помощь
@dp.message_handler(lambda message: help_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    button = get_button(help_button.number)
    message_text = get_message(button).text
    await state.finish()
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=start_kb)


# Назад
@dp.message_handler(lambda message: back_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'Назад', parse_mode='Markdown', reply_markup=start_kb)


# Личный кабинет
@dp.message_handler(lambda message: account_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    user_profile = get_profile(message.from_user.id)
    message_text = f"""
    Здраствуйте, {user_profile.name}!
Ваш баланс - {user_profile.balance} рублей
Количество рефералов - {user_profile.referral_count}
Доход от рефералов - {user_profile.referral_balance} рублей
    """
    await state.finish()
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=personal_area_kb)


@dp.message_handler(lambda message: add_balance.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    button = get_button(add_balance.number)
    message_text = get_message(button).text
    await Form.input_amount_add_balance.set()
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=personal_area_kb)


@dp.message_handler(state=Form.input_amount_add_balance)
@save_message
async def help_message(message: types.Message, state: FSMContext, raw_state):
    try:
        amount = int(message.text)

        pay = qiwi.create_pay(amount)

        inline_qiwi_btn = InlineKeyboardButton('QIWI', url=pay['link'])
        inline_kb = InlineKeyboardMarkup().add(inline_qiwi_btn)

        await bot.send_message(message.from_user.id, 'Отлично, переходите к оплате!', parse_mode='Markdown', reply_markup=inline_kb)
        await state.finish()
        timer = time.time()
        while True:
            await asyncio.sleep(20)
            if qiwi.check_pay(pay['build']):
                user_profile = get_profile(message.from_user.id)
                user_profile.balance = user_profile.balance + amount
                user_profile.save()
                break
            if time.time() - timer > 3000:
                break

    except ValueError:
        await bot.send_message(message.from_user.id, 'Введите целое число!', parse_mode='Markdown',
                               reply_markup=personal_area_kb)


@dp.message_handler(lambda message: ref_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    user_profile = get_profile(message.from_user.id)
    button = get_button(ref_button.number)
    message_text = get_message(button).text.replace('REF', user_profile.ref)
    await state.finish()
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=personal_area_kb)


# Ветка Заказов
@dp.message_handler(lambda message: orders_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    button = get_button(orders_button.number)
    message_text = get_message(button).text
    await state.finish()
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=orders_kb)


# Активные заказы
@dp.message_handler(lambda message: orders_active_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    user_profile = get_profile(message.from_user.id)
    for i in get_active_orders(user_profile):
        order_message = f'{i.platform} - {i.type} - {i.count}'
        await bot.send_message(message.from_user.id, order_message, parse_mode='Markdown', reply_markup=orders_kb)
    await state.finish()


# Все заказы
@dp.message_handler(lambda message: orders_archive_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    user_profile = get_profile(message.from_user.id)
    for i in get_active_orders(user_profile):
        order_message = f'{i.platform} - {i.type} - {i.count} - {i.status}'
        await bot.send_message(message.from_user.id, order_message, parse_mode='Markdown', reply_markup=orders_kb)
    await state.finish()
# Конец ветки Заказов


# Ветка Раскрутки
@dp.message_handler(lambda message: promotion_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    button = get_button(promotion_button.number)
    message_text = get_message(button).text
    await state.finish()
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=service_kb)


# Раскутка Ветка Инстаграмма
@dp.message_handler(lambda message: instagram_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    button = get_button(promotion_button.number)
    message_text = get_message(button).text
    await state.finish()
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=instagram)


@dp.message_handler(lambda message: instagram_sub_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    button = get_button(instagram_sub_button.number)
    info = get_service_info("Instagram", 'Подписчики')
    message_text = get_message(button).text.replace('PRICE', f'{info.price*1000}').\
        replace('MIN', f'{info.min_count}').replace('MAX', f'{info.max_count}')
    await Form.input_amount_service.set()
    await state.update_data(info=info)
    await state.update_data(keyboard=instagram)
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=instagram)


@dp.message_handler(lambda message: instagram_like_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    button = get_button(instagram_sub_button.number)
    info = get_service_info("Instagram", 'Лайки')
    message_text = get_message(button).text.replace('PRICE', f'{info.price*1000}').\
        replace('MIN', f'{info.min_count}').replace('MAX', f'{info.max_count}')
    await Form.input_amount_service.set()
    await state.update_data(info=info)
    await state.update_data(keyboard=instagram)
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=instagram)


@dp.message_handler(lambda message: instagram_story_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    button = get_button(instagram_sub_button.number)
    info = get_service_info("Instagram", 'Просмотры сторис')
    message_text = get_message(button).text.replace('PRICE', f'{info.price*1000}').\
        replace('MIN', f'{info.min_count}').replace('MAX', f'{info.max_count}')
    await Form.input_amount_service.set()
    await state.update_data(info=info)
    await state.update_data(keyboard=instagram)
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=instagram)

# Раскутка Конец Ветки Инстаграмма


# Раскутка Ветка Тик-Ток
@dp.message_handler(lambda message: tik_tok_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    button = get_button(promotion_button.number)
    message_text = get_message(button).text
    await state.finish()
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=tik_tok)


@dp.message_handler(lambda message: tik_tok_sub_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    button = get_button(instagram_sub_button.number)
    info = get_service_info("Instagram", 'Подписчики')
    message_text = get_message(button).text.replace('PRICE', f'{info.price*1000}').\
        replace('MIN', f'{info.min_count}').replace('MAX', f'{info.max_count}')
    await Form.input_amount_service.set()
    await state.update_data(info=info)
    await state.update_data(keyboard=instagram)
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=instagram)

# Раскутка Конец Ветки Тик-Тока


# Раскутка Ветка ВКонтакте
@dp.message_handler(lambda message: vk_button.text in message.text, state="*")
@check_button
@save_message
async def help_message(message: types.Message, state: FSMContext):
    button = get_button(promotion_button.number)
    message_text = get_message(button).text
    await state.finish()
    await bot.send_message(message.from_user.id, message_text, parse_mode='Markdown', reply_markup=vk)
# Раскутка Конец Ветки ВКонтакте

# Общий функционал для ветки Раскрутка


@dp.message_handler(state=Form.input_amount_service)
@save_message
async def help_message(message: types.Message, state: FSMContext, raw_state):
    try:
        user_data = await state.get_data()
        info = user_data['info']
        amount = int(message.text.replace(' ', ''))
        if amount > int(info.max_count):
            await bot.send_message(message.from_user.id, f'Слишко много! Максимум - {info.max_count}',
                                   parse_mode='Markdown')
        elif amount < int(info.min_count):
            await bot.send_message(message.from_user.id, f'Слишко мало! Минимум - {info.min_count}',
                                   parse_mode='Markdown')
        else:
            await bot.send_message(message.from_user.id, f'Отлично! Введите ссылку в формате {info.link_form}!',
                                   parse_mode='Markdown')
            await state.update_data(amount=amount)
            await Form.input_link.set()
    except ValueError:
        await bot.send_message(message.from_user.id, 'Введите целое число!', parse_mode='Markdown',
                               reply_markup=personal_area_kb)


@dp.message_handler(state=Form.input_link)
@save_message
async def help_message(message: types.Message, state: FSMContext, raw_state):

    user_data = await state.get_data()
    info = user_data['info']
    if info.link_form in message.text:
        await bot.send_message(message.from_user.id, f'Всё отлично! Услуга будет стоить {info.price*info["amount"]}.'
                                                     f' Эта сумма будет списана с вашего счёта. Вы уверены?',
                                                     parse_mode='Markdown', reply_markup=user_data['keyboard'])
        await state.update_data(link=message.text.strip(' '))
        await Form.check.set()
    else:
        await bot.send_message(message.from_user.id, f'Попробуйте ещё! Нет тот формат ссылки. ссылка должна быть'
                                                     f' в форме {info.link_form}', parse_mode='Markdown',
                                                     reply_markup=user_data['keyboard'])


@dp.message_handler(state=Form.check)
@save_message
async def help_message(message: types.Message, state: FSMContext, raw_state):

    user_data = await state.get_data()
    info = user_data['info']
    if info.link_form in message.text:
        await bot.send_message(message.from_user.id, 'Всё отлично! Начинаем услугу!', parse_mode='Markdown',
                               reply_markup=user_data['keyboard'])
        await state.update_data(link=message.text.strip(' '))
    else:
        await bot.send_message(message.from_user.id, f'Попробуйте ещё! Нет тот формат ссылки. ссылка должна быть в форме'
                                                     f' {info.link_form}', parse_mode='Markdown',
                                                     reply_markup=user_data['keyboard'])



# Конец общего функционала для ветки Раскрутка

# Конец ветки Раскрутки


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        executor.start_polling(dp, on_shutdown=shutdown)




