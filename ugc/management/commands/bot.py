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


def check_category(user: Profile, work_type: WorkType):
    resume = Resume.objects.filter(user=user)
    result = WorkTypeResume.objects.filter(resume=resume, work_type=work_type)
    if len(result) == 0:
        return False
    else:
        return result[0]


def create_keyboard(list_id: list):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for button_id in list_id:
        button_request = get_button(button_id)
        if button_request.status is True:
            button = KeyboardButton(button_request.text)
            kb.add(button)
    return kb


def inline_keyboard(list_id: list):
    kb = InlineKeyboardMarkup()
    for button in list_id:
        button_request = get_button(button)
        if button_request.status is True:
            button = InlineKeyboardButton(button_request.text, callback_data=button_request.text)
            kb.add(button)
    return kb


def inline_keyboard_work(search=False, new=False):
    if search is True:
        type_work = 'search'
    elif new is True:
        type_work = 'new'
    else:
        type_work = 'work_type'
    kb = InlineKeyboardMarkup()
    work_list = WorkType.objects.filter(relates_to=None)
    for work in work_list:
        inline_btn = InlineKeyboardButton(work.type_name, callback_data=f'{type_work} @{work.type_name}')
        kb.add(inline_btn)
    return kb


def save_keyboard(func):
    async def wrapper(*args, **kwargs):
        try:
            print(*args)
            keyboard = await func(*args, **kwargs)
            print(keyboard)
            await kwargs['state'].update_data(keyboard=keyboard)
        except Exception as e:
            print(e)
    return wrapper


token = settings.TOKEN

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

no_employee_list = [3, 4, 23, 20]
employee_list = [24, 6, 5, 20]
employee_profile_list = [12, 13, 14, 15, 16, 17, 7]

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
main_menu = get_button(20)
change_photo = get_button(22)
create_order = get_button(23)
my_resume = get_button(24)


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
@save_keyboard
async def start_message(message: types.Message, state: FSMContext, **kwargs):
    profile = get_profile(message.from_user.id)
    if profile is False:
        Profile.objects.create(external_id=message.from_user.id, name=message.from_user.username)
    msg = get_message(1)
    keyboard = create_keyboard([1, 2])
    await bot.send_message(message.from_user.id, msg.text, reply_markup=keyboard, parse_mode='Markdown')
    return keyboard


@dp.message_handler(lambda message: main_menu.text in message.text, state="*")
@save_keyboard
async def start_message(message: types.Message, state: FSMContext, **kwargs):
    profile = get_profile(message.from_user.id)
    if profile is False:
        Profile.objects.create(external_id=message.from_user.id, name=message.from_user.username)
    msg = get_message(1)
    keyboard = create_keyboard([1, 2])
    await bot.send_message(message.from_user.id, msg.text, reply_markup=keyboard, parse_mode='Markdown')
    return keyboard


@dp.callback_query_handler(lambda c: main_menu.text in c.data)
@save_keyboard
async def start_message(message: types.Message, state: FSMContext, **kwargs):
    profile = get_profile(message.from_user.id)
    if profile is False:
        Profile.objects.create(external_id=message.from_user.id, name=message.from_user.username)
    msg = get_message(1)
    keyboard = create_keyboard([1, 2])
    await bot.send_message(message.from_user.id, msg.text, reply_markup=keyboard, parse_mode='Markdown')
    return keyboard


@dp.message_handler(lambda message: cancel.text in message.text, state="*")
@save_keyboard
async def help_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await state.finish()
    msg = get_message(35)
    keyboard = user_data['keyboard']
    await bot.send_message(message.from_user.id, msg.text, reply_markup=keyboard, parse_mode='Markdown')
    return keyboard


@dp.message_handler(lambda message: no_employee.text in message.text, state="*")
@save_keyboard
async def help_message(message: types.Message, state: FSMContext):
    msg = get_message(3)
    keyboard = create_keyboard(no_employee_list)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.message_handler(lambda message: new_work.text in message.text, state="*")
@save_keyboard
async def help_message(message: types.Message, state: FSMContext):
    msg = get_message(18)
    keyboard = inline_keyboard_work(search=True)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.callback_query_handler(lambda c: 'search' in c.data)
async def process_callback_sad(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.answer_callback_query(callback_query.id)
    work_type = str(callback_query.data).split('@')[1]
    obj = WorkType.objects.filter(type_name=work_type)[0]
    if obj.subtype_status is True:
        kb = InlineKeyboardMarkup()
        for work in WorkType.objects.filter(relates_to=obj):
            inline_btn = InlineKeyboardButton(work.type_name, callback_data=f'search @{work.type_name}')
            kb.add(inline_btn)
        await bot.send_message(callback_query.from_user.id, 'Уточните...', reply_markup=kb)
        return
    resumes = list(WorkTypeResume.objects.filter(work_type=obj))

    # Проверка на доступ к резюме
    for i in resumes:
        if i.resume.status is False:
            resumes.pop(resumes.index(i))

    if len(resumes) == 0:
        msg = get_message(30)
        await bot.send_message(callback_query.from_user.id, msg.text)
        return
    msg = get_message(19)
    await bot.send_message(callback_query.from_user.id, msg.text)
    for i in resumes:
        final_message = i.resume.content + '\n\n\n' + i.resume.user.contacts
        if i.resume.user.photo:
            await bot.send_photo(callback_query.from_user.id, open(i.resume.user.photo.path, 'rb'), caption=final_message,
                                 parse_mode='Markdown')

        else:
            await bot.send_message(callback_query.from_user.id, final_message)


@dp.message_handler(lambda message: create_order.text in message.text, state="*")
@save_keyboard
async def help_message(message: types.Message, state: FSMContext):
    await state.finish()
    msg = get_message(26)
    keyboard = inline_keyboard_work(new=True)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.callback_query_handler(lambda c: 'new' in c.data)
async def process_callback_sad(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.answer_callback_query(callback_query.id)
    work_type = str(callback_query.data).split('@')[1]
    obj = WorkType.objects.filter(type_name=work_type)[0]
    if obj.subtype_status is True:
        kb = InlineKeyboardMarkup()
        for work in WorkType.objects.filter(relates_to=obj):
            inline_btn = InlineKeyboardButton(work.type_name, callback_data=f'new @{work.type_name}')
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
    Order.objects.create(user=profile, content=message.text, work_type=work_type)
    keyboard = create_keyboard(no_employee_list)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    work_type_resumes = WorkTypeResume.objects.filter(work_type=work_type)
    for work_type_resume in work_type_resumes:
        resume = work_type_resume.resume
        if resume.user.notification is True:
            full_text = message.text + "\n\n" + '@' + str(message.from_user.username)
            await bot.send_message(resume.user.external_id, full_text)


@dp.message_handler(lambda message: employee.text in message.text, state="*")
@save_keyboard
async def help_message(message: types.Message, state: FSMContext):
    msg = get_message(2)
    keyboard = create_keyboard(employee_list)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.callback_query_handler(lambda c: notification_setting.text in c.data)
async def help_message(message: types.Message, state: FSMContext):
    msg = get_message(6)
    keyboard = create_keyboard([9, 10, 8])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.message_handler(lambda message: notification_on.text in message.text, state="*")
@save_keyboard
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    profile.notification = True
    profile.save()
    msg = get_message(7)
    keyboard = create_keyboard(employee_list)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.message_handler(lambda message: notification_off.text in message.text, state="*")
@save_keyboard
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    profile.notification = False
    profile.save()
    msg = get_message(8)
    keyboard = create_keyboard(employee_list)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.message_handler(lambda message: my_resume.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    resume = get_resume(profile)
    msg = get_message(31)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown')
    final_message = resume.content + '\n\n\n' + resume.user.contacts

    if resume.user.photo:
        await bot.send_photo(message.from_user.id, open(resume.user.photo.path, 'rb'), caption=final_message,
                             parse_mode='Markdown')

    else:
        await bot.send_message(message.from_user.id, final_message)
    if resume.status is True:
        msg = get_message(33)
        await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown')
    else:
        msg = get_message(34)
        await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown')


@dp.message_handler(lambda message: resume_create.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    await Form.input_resume_text.set()
    msg = get_message(5)
    keyboard = create_keyboard([8])
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.message_handler(state=Form.input_resume_text)
async def help_message(message: types.Message, state: FSMContext, raw_state):
    print('Input go')
    profile = get_profile(message.from_user.id)
    resume = get_resume(profile)
    if resume is False:
        Resume.objects.create(user=profile, content=message.text)
    else:
        resume.content = message.text
        resume.status = False
        resume.save()
    msg = get_message(9)
    keyboard = inline_keyboard_work()
    clear_work_type(profile)
    await state.finish()
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.callback_query_handler(lambda c: 'work_type' in c.data)
async def process_callback_sad(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.answer_callback_query(callback_query.id)
    work_type = str(callback_query.data).split('@')[1]
    obj = WorkType.objects.filter(type_name=work_type)[0]
    if obj.subtype_status is True:
        kb = InlineKeyboardMarkup()
        for work in WorkType.objects.filter(relates_to=obj):
            inline_btn = InlineKeyboardButton(work.type_name, callback_data=f'work_type @{work.type_name}')
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
    keyboard = create_keyboard([11])
    profile = get_profile(callback_query.from_user.id)
    resume = get_resume(profile)
    work_type = get_work_type(work_type)
    if len(WorkTypeResume.objects.filter(work_type=work_type, resume=resume)) == 0:
        WorkTypeResume.objects.create(work_type=work_type, resume=resume, content='')
        msg = get_message(32)
        await bot.send_message(callback_query.from_user.id, msg.text, reply_markup=keyboard)
        return keyboard
    else:
        msg = get_message(36)
        await bot.send_message(callback_query.from_user.id, msg.text, reply_markup=keyboard)
        return keyboard


@dp.message_handler(lambda message: work_type_final.text in message.text, state="*")
@save_keyboard
async def help_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    msg = get_message(10)
    keyboard = create_keyboard(employee_list)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.message_handler(lambda message: employee_profile.text in message.text, state="*")
@save_keyboard
async def help_message(message: types.Message, state: FSMContext):
    msg = get_message(11)
    keyboard = inline_keyboard(employee_profile_list)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.message_handler(lambda message: rating.text in message.text, state="*")
@save_keyboard
async def help_message(message: types.Message, state: FSMContext):
    msg = get_message(11)
    keyboard = create_keyboard(employee_profile_list)
    await bot.send_message(message.from_user.id, "На данный момемент этот раздел не доступен",
                           parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.callback_query_handler(lambda c: language.text in c.data)
@save_keyboard
async def help_message(message: types.Message, state: FSMContext, raw_state):
    profile = get_profile(message.from_user.id)
    msg = get_message(11)
    keyboard = create_keyboard(employee_profile_list)
    await bot.send_message(message.from_user.id, "На данный момемент этот раздел не доступен",
                           parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.callback_query_handler(lambda c: city.text in c.data)
@save_keyboard
async def help_message(message: types.Message, state: FSMContext, raw_state):
    profile = get_profile(message.from_user.id)
    if profile is False:
        await bot.send_message(message.from_user.id, 'Вам это не доступно!', parse_mode='Markdown')
        return
    msg = get_message(11)
    keyboard = create_keyboard(employee_profile_list)
    await bot.send_message(message.from_user.id, "На данный момемент этот раздел не доступен",
                           parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.callback_query_handler(lambda c: contacts.text in c.data)
async def help_message(message: types.Message, state: FSMContext, raw_state):
    profile = get_profile(message.from_user.id)
    msg = get_message(12).text
    if profile.contacts != "":
        msg = msg + f'\n\n {profile.contacts}'
    else:
        msg = get_message(13).text
    keyboard = create_keyboard([18, 8])
    await bot.send_message(message.from_user.id, msg,
                           parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.message_handler(lambda message: change_contacts.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    msg = get_message(14).text
    await Form.input_contacts.set()
    await bot.send_message(message.from_user.id, msg, parse_mode='Markdown')


@dp.message_handler(state=Form.input_contacts)
@save_keyboard
async def help_message(message: types.Message, state: FSMContext, raw_state):
    profile = get_profile(message.from_user.id)
    msg = get_message(15)
    profile.contacts = message.text
    profile.save()
    await state.finish()
    keyboard = inline_keyboard(employee_profile_list)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.callback_query_handler(lambda c: category.text in c.data)
async def help_message(message: types.Message, state: FSMContext, raw_state):
    profile = get_profile(message.from_user.id)
    resume = get_resume(profile)
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
    return keyboard


@dp.message_handler(lambda message: change_category.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    profile = get_profile(message.from_user.id)
    msg = get_message(9).text
    keyboard = inline_keyboard_work()
    clear_work_type(profile)
    await state.finish()
    await bot.send_message(message.from_user.id, msg, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


@dp.callback_query_handler(lambda c: photo.text in c.data)
async def help_message(message: types.Message, state: FSMContext, raw_state):
    profile = get_profile(message.from_user.id)
    keyboard = create_keyboard([22, 8])
    if profile.photo == '':
        msg = get_message(20).text
        await bot.send_message(message.from_user.id, msg, parse_mode='Markdown', reply_markup=keyboard)
        return
    msg = get_message(21).text
    await bot.send_photo(message.from_user.id, open(profile.photo.path, 'rb'), caption=msg, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard

#     await Form.input_photo.set()


@dp.message_handler(lambda message: change_photo.text in message.text, state="*")
async def help_message(message: types.Message, state: FSMContext):
    msg = get_message(22).text
    await Form.input_photo.set()
    await bot.send_message(message.from_user.id, msg, parse_mode='Markdown')


@dp.message_handler(state=Form.input_photo, content_types=['document', 'photo'])
@save_keyboard
async def help_message(message: types.Message, state: FSMContext, raw_state):
    profile = get_profile(message.from_user.id)
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
    keyboard = inline_keyboard(employee_profile_list)
    await bot.send_message(message.from_user.id, msg.text, parse_mode='Markdown', reply_markup=keyboard)
    return keyboard


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        executor.start_polling(dp, on_shutdown=shutdown)
