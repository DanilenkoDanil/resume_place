from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from ugc.models import BotMessage, BotButton, Profile, Resume, WorkType, WorkTypeResume, Order
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
    return BotButton.objects.filter(id=button_id)[0]


def get_message(message_id: int):
    return BotMessage.objects.filter(id=message_id)[0]


def get_profile(telegram_id: int):
    result = Profile.objects.filter(external_id=telegram_id)
    if len(result) == 0:
        return False
    else:
        return result[0]


def clear_work_type(user: Profile):
    resume = get_resume(user)
    result = WorkTypeResume.objects.filter(resume=resume)
    for i in result:
        i.delete()


def get_work_type(name: str):
    result = WorkType.objects.filter(type_name=name)
    if len(result) == 0:
        return False
    else:
        return result[0]


def get_resume(user: Profile):
    result = Resume.objects.filter(user=user)
    if len(result) == 0:
        return False
    else:
        return result[0]


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


def inline_keyboard_work(search=False, new=True):
    if search is True:
        type_work = 'search'
    elif new is True:
        type_work = 'new'
    else:
        type_work = 'work_type'
    kb = InlineKeyboardMarkup()
    work_list = WorkType.objects.filter(relates_to=None)
    for work in work_list:
        inline_btn = InlineKeyboardButton(work.type_name, callback_data=f'{type_work} {work.type_name}')
        kb.add(inline_btn)
    return kb


token = settings.TOKEN

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

no_employee = get_button(1)
employee = get_button(2)
my_work = get_button(3)
new_work = get_button(4)
resume_create = get_button(5)
employee_profile = get_button(6)
cancel = get_button(8)
notification_setting = get_button(7)
notification_on = get_button(9)
notification_off = get_button(10)
work_type_final = get_button(11)
rating = get_button(12)
language = get_button(13)
city = get_button(14)
contacts = get_button(15)
change_contacts = get_button(18)
category = get_button(17)
change_category = get_button(21)
photo = get_button(16)
change_photo = get_button(22)
create_order = get_button(23)


class Form(StatesGroup):
    input_resume_text = State()
    input_work_type = State()
    input_contacts = State()
    input_photo = State()
    input_order_content = State()


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


@dp.message_handler(commands=['start'], state="*")
async def start_message(message: types.Message, state: FSMContext, **kwargs):
    msg = get_message(1)
    first_kb = create_keyboard([1, 2])
    await bot.send_message(message.from_user.id, msg.text, reply_markup=first_kb, parse_mode='Markdown')


@dp.message_handler(lambda message: cancel.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        msg = get_message(1)
        first_kb = create_keyboard([1, 2])
        await bot.send_message(message.from_user.id, msg.text, reply_markup=first_kb, parse_mode='Markdown')
    else:
        if profile.employee is True:
            keyboard = create_keyboard([5, 6, 7])
            await bot.send_message(message.from_user.id, 'Вы работник', parse_mode='Markdown', reply_markup=keyboard)
        else:
            keyboard = create_keyboard([3, 4, 23])
            await bot.send_message(message.from_user.id, 'Вы ищите работника', parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: no_employee.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        Profile.objects.create(external_id=message.from_user.id, employee=True, name=message.from_user.username)
    msg = get_message(3)
    keyboard = create_keyboard([3, 4, 23])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: new_work.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    msg = get_message(18)
    kb = inline_keyboard_work(search=True)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=kb)


@dp.callback_query_handler(lambda c: 'search' in c.data)
async def process_callback_sad(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    print('sda')
    await bot.answer_callback_query(callback_query.id)
    work_type = str(callback_query.data).split(' ')[1]
    print(work_type)
    obj = WorkType.objects.filter(type_name=work_type)[0]
    print(obj)
    if obj.subtype_status is True:
        kb = InlineKeyboardMarkup()
        print('2')
        for work in WorkType.objects.filter(relates_to=obj):
            print('+')
            inline_btn = InlineKeyboardButton(work.type_name, callback_data=f'search {work.type_name}')
            kb.add(inline_btn)
        await bot.send_message(callback_query.from_user.id, 'Уточните...', reply_markup=kb)
        return
    resumes = WorkTypeResume.objects.filter(work_type=obj)
    msg = get_message(19)
    await bot.send_message(callback_query.from_user.id, msg.text)
    for i in resumes:
        final_message = i.resume.content + '\n\n\n' + i.resume.user.contacts
        if i.resume.user.photo is None:
            await bot.send_message(callback_query.from_user.id, final_message)
        else:
            await bot.send_photo(callback_query.from_user.id, open(i.resume.user.photo.path, 'rb'), caption=final_message,
                                 parse_mode='Markdown')


@dp.message_handler(lambda message: create_order.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    msg = get_message(26)
    kb = inline_keyboard_work(new=True)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=kb)


@dp.callback_query_handler(lambda c: 'new' in c.data)
async def process_callback_sad(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    print('sda')
    await bot.answer_callback_query(callback_query.id)
    work_type = str(callback_query.data).split(' ')[1]
    print(work_type)
    obj = WorkType.objects.filter(type_name=work_type)[0]
    print(obj)
    if obj.subtype_status is True:
        kb = InlineKeyboardMarkup()
        print('2')
        for work in WorkType.objects.filter(relates_to=obj):
            print('+')
            inline_btn = InlineKeyboardButton(work.type_name, callback_data=f'new {work.type_name}')
            kb.add(inline_btn)
        await bot.send_message(callback_query.from_user.id, 'Уточните...', reply_markup=kb)
        return
    await state.update_data(work_type=obj)
    msg = get_message(27)
    await Form.input_order_content.set()
    await bot.send_message(callback_query.from_user.id, msg.text)


@dp.message_handler(state=Form.input_order_content)
async def help_message(message: types.Message, state: FSMContext, raw_state):
    profile = get_profile(message.from_user.id)
    user_data = await state.get_data()
    work_type = user_data['work_type']
    msg = get_message(28)
    await state.finish()
    Order.objects.create(user=profile, content=message.text)
    keyboard = create_keyboard([3, 4, 23])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    work_type_resumes = WorkTypeResume.objects.filter(work_type=work_type)
    for work_type_resume in work_type_resumes:
        resume = work_type_resume.resume
        if resume.user.notification is True:
            full_text = message.text + "\n\n" + '@' + str(message.from_user.username)
            await bot.send_message(resume.user.external_id, full_text)


@dp.message_handler(lambda message: employee.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        Profile.objects.create(external_id=message.from_user.id, employee=True, name=message.from_user.username)
    msg = get_message(2)
    keyboard = create_keyboard([5, 6, 7])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: no_employee.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is not False:
        await bot.send_message(message.from_user.id, 'Вы уже зарегестрированы!', parse_mode='Markdown')
    msg = get_message(3)
    Profile.objects.create(external_id=message.from_user.id, employee=False, name=message.from_user.username)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown')


@dp.message_handler(lambda message: notification_setting.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    msg = get_message(6)
    keyboard = create_keyboard([9, 10, 8])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: notification_on.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    profile.notification = True
    profile.save()
    msg = get_message(7)
    if profile.employee is True:
        keyboard = create_keyboard([5, 6, 7])
    else:
        keyboard = create_keyboard([3, 4])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: notification_off.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    profile.notification = False
    profile.save()
    msg = get_message(8)
    if profile.employee is True:
        keyboard = create_keyboard([5, 6, 7])
    else:
        keyboard = create_keyboard([3, 4])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: resume_create.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    if profile.employee is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    await Form.input_resume_text.set()
    msg = get_message(5)
    keyboard = create_keyboard([8])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(state=Form.input_resume_text)
async def help_message(message: types.Message, state: FSMContext, raw_state):
    profile = get_profile(message.from_user.id)
    resume = get_resume(profile)
    if resume is False:
        Resume.objects.create(user=profile, content=message.text)
    else:
        resume.content = message.text
        resume.status = False
        resume.save()
    msg = get_message(9)
    kb = inline_keyboard_work()
    clear_work_type(profile)
    await state.finish()
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=kb)


@dp.callback_query_handler(lambda c: 'work_type' in c.data)
async def process_callback_sad(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    print('sda')
    await bot.answer_callback_query(callback_query.id)
    work_type = str(callback_query.data).split(' ')[1]
    print(work_type)
    obj = WorkType.objects.filter(type_name=work_type)[0]
    print(obj)
    if obj.subtype_status is True:
        kb = InlineKeyboardMarkup()
        print('2')
        for work in WorkType.objects.filter(relates_to=obj):
            print('+')
            inline_btn = InlineKeyboardButton(work.type_name, callback_data=f'work_type {work.type_name}')
            kb.add(inline_btn)
        await bot.send_message(callback_query.from_user.id, 'Уточните...', reply_markup=kb)
        return
    user_data = await state.get_data()
    if user_data.get('work_type') is None:
        result = [work_type]
    else:
        if work_type not in user_data['work_type']:
            result = user_data['work_type']
            result.append(work_type)
        else:
            result = user_data['work_type']
    await state.update_data(work_type=result)
    user_data = await state.get_data()
    print(user_data['work_type'])
    keyboard = create_keyboard([11])
    profile = get_profile(callback_query.from_user.id)
    resume = get_resume(profile)
    work_type = get_work_type(work_type)
    WorkTypeResume.objects.create(work_type=work_type, resume=resume, content='')
    await bot.send_message(callback_query.from_user.id, 'Принято', reply_markup=keyboard)


@dp.message_handler(lambda message: work_type_final.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    if profile.employee is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    user_data = await state.get_data()
    print(user_data['work_type'])
    msg = get_message(10)
    keyboard = create_keyboard([5, 6, 7])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: employee_profile.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    if profile.employee is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    msg = get_message(11)
    keyboard = create_keyboard([12, 13, 14, 15, 16, 17, 8])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: rating.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    if profile.employee is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    msg = get_message(11)
    keyboard = create_keyboard([12, 13, 14, 15, 16, 17, 8])
    await bot.send_message(message.from_user.id, "На данный момемент этот раздел не доступен",
                           parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: rating.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    if profile.employee is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    msg = get_message(11)
    keyboard = create_keyboard([12, 13, 14, 15, 16, 17, 8])
    await bot.send_message(message.from_user.id, "На данный момемент этот раздел не доступен",
                           parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: language.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    if profile.employee is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    msg = get_message(11)
    keyboard = create_keyboard([12, 13, 14, 15, 16, 17, 8])
    await bot.send_message(message.from_user.id, "На данный момемент этот раздел не доступен",
                           parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: city.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    if profile.employee is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    msg = get_message(11)
    keyboard = create_keyboard([12, 13, 14, 15, 16, 17, 8])
    await bot.send_message(message.from_user.id, "На данный момемент этот раздел не доступен",
                           parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: contacts.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    if profile.employee is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    msg = get_message(12).text
    if profile.contacts != "":
        msg = msg + f'\n\n {profile.contacts}'
    else:
        msg = get_message(13).text
    keyboard = create_keyboard([18, 8])
    await bot.send_message(message.from_user.id, msg,
                           parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: change_contacts.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    if profile.employee is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    msg = get_message(14).text
    await Form.input_contacts.set()
    await bot.send_message(message.from_user.id, msg, parse_mode='Markdown')


@dp.message_handler(state=Form.input_contacts)
async def help_message(message: types.Message, state: FSMContext, raw_state):
    profile = get_profile(message.from_user.id)
    msg = get_message(15)
    profile.contacts = message.text
    profile.save()
    await state.finish()
    keyboard = create_keyboard([12, 13, 14, 15, 16, 17, 8])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(lambda message: category.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    resume = get_resume(profile)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    if profile.employee is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    result = WorkTypeResume.objects.filter(resume=resume)
    if len(result) == 0:
        keyboard = create_keyboard([21, 8])
        msg = get_message(17).text
        await bot.send_message(message.from_user.id, msg, parse_mode='Markdown', reply_markup=keyboard)
    else:
        keyboard = create_keyboard([21, 8])
        msg = get_message(16).text
        await bot.send_message(message.from_user.id, msg, parse_mode='Markdown', reply_markup=keyboard)
        for i in result:
            await bot.send_message(message.from_user.id, str(i.work_type.type_name), parse_mode='Markdown')


@dp.message_handler(lambda message: category.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    resume = get_resume(profile)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    if profile.employee is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    result = WorkTypeResume.objects.filter(resume=resume)
    if len(result) == 0:
        keyboard = create_keyboard([21, 8])
        msg = get_message(17).text
        await bot.send_message(message.from_user.id, msg, parse_mode='Markdown', reply_markup=keyboard)
    else:
        keyboard = create_keyboard([21, 8])
        msg = get_message(16).text
        await bot.send_message(message.from_user.id, msg, parse_mode='Markdown', reply_markup=keyboard)
        for i in result:
            await bot.send_message(message.from_user.id, str(i.work_type.type_name), parse_mode='Markdown')


@dp.message_handler(lambda message: change_category.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    if profile.employee is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return

    msg = get_message(9).text
    kb = inline_keyboard_work()
    clear_work_type(profile)
    await state.finish()
    await bot.send_message(message.from_user.id, msg, parse_mode='Markdown', reply_markup=kb)


@dp.message_handler(lambda message: photo.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    keyboard = create_keyboard([22, 8])
    if profile.photo is None:
        msg = get_message(20).text
        await bot.send_message(message.from_user.id, msg, parse_mode='Markdown', reply_markup=keyboard)
        return
    msg = get_message(21).text
    await bot.send_photo(message.from_user.id, open(profile.photo.path, 'rb'), caption=msg, parse_mode='Markdown', reply_markup=keyboard)

#     await Form.input_photo.set()


@dp.message_handler(lambda message: change_photo.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    msg = get_message(22).text
    await Form.input_photo.set()
    await bot.send_message(message.from_user.id, msg, parse_mode='Markdown')


@dp.message_handler(state=Form.input_photo, content_types=['document', 'photo'])
async def help_message(message: types.Message, state: FSMContext, raw_state):
    profile = get_profile(message.from_user.id)
    print('!!!!!!!!!!!!!!!!!!')
    if message.document is None:
        await bot.download_file_by_id(message.photo[-1].file_id, 'test.png')
        profile.photo = File(open('test.png', 'rb'))
        profile.save()
    else:
        if str(message.document.file_name).split('.')[-1] in ['jpg', 'png']:
            await bot.download_file_by_id(message.document.file_id, 'test.png')
            profile.photo = File(open('test.png', 'rb'))
            profile.save()
        else:
            msg = get_message(25)
            await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown')
            return
    msg = get_message(23)
    await state.finish()
    keyboard = create_keyboard([12, 13, 14, 15, 16, 17, 8])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        executor.start_polling(dp, on_shutdown=shutdown)




