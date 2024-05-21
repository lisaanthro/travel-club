import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import StatesGroup

from http import HTTPStatus

from config_reader import config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State
from aiogram.types import ReplyKeyboardRemove
from keyboards import *
from aiogram.filters import StateFilter
import requests
import json

s = requests.session()

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


# storage = MemoryStorage()

class FSM(StatesGroup):
    auth_next = State()
    sign_in_next = State()
    # sign_in_password_next = State()
    sign_up_next = State()
    # sign_up_name_next = State()
    sign_up_password_next = State()
    main_menu_keyboard = State()
    main_menu_next = State()
    profile_choice = State()
    change_profile_next = State()
    request_change_profile_next = State()
    get_item_info_for_rent_next = State()
    get_item_info_for_return_next = State()
    rent_next = State()
    return_next = State()


@dp.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        'Привет, я - бот-помощник туристического клуба университета МИСИС. Помогаю арендовывать снаряжение. \nДля '
        'работы со мной необходимо войти в аккаунт или зарегистрироваться.\nДо встречи в аккаунте!',
        reply_markup=start_keyboard)
    await state.set_state(FSM.auth_next)


@dp.message(F.text == "Вход", FSM.auth_next)
async def sigh_in(message: types.Message, state: FSMContext):
    await message.answer('Введите почту и пароль через пробел',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSM.sign_in_next)


@dp.message(F.text == "Регистрация", FSM.auth_next)
async def sigh_up(message: types.Message, state: FSMContext):
    await message.answer('Введите почту, имя и пароль через пробелы в соответствующем порядке')
    await state.set_state(FSM.sign_up_next)


@dp.message(F.text.contains('@'), FSM.sign_up_next)
async def post_mail_name_password(message: types.Message, state: FSMContext):
    # url = 'https://gear.dino-misis.ru/user/register'
    url = 'http://127.0.0.1:8000/user/register'
    email, name, password = message.text.split()
    payload = {'email': email, 'name': name, 'password': password}
    token = s.post(url, json=payload).json().get('bearer_token')
    s.headers = {'Authorization': f'Bearer {token}'}
    print('registered')

    await message.answer('Данные приняты', reply_markup=main_keyboard)
    await state.set_state(FSM.main_menu_next)


@dp.message(F.text.contains('@'), FSM.sign_in_next)
async def post_mail_password(message: types.Message, state: FSMContext):
    # url = 'https://gear.dino-misis.ru/user/login'
    url = 'http://127.0.0.1:8000/user/login'
    email, password = message.text.split()
    payload = {'email': email, 'password': password}
    response = s.post(url, json=payload)
    if response.status_code == HTTPStatus.OK:
        token = response.json().get('bearer_token')
        s.headers = {'Authorization': f'Bearer {token}'}
        print('logged in', s.headers)

        await message.answer('Вход выполнен', reply_markup=main_keyboard)
        await state.set_state(FSM.main_menu_next)
    else:
        await message.answer(str(response.content))


# @dp.message(FSM.main_menu_keyboard)
# def main_menu_keyboard(message: types.Message):
#     await message.answer(text='Главное меню', reply_markup=main_keyboard)


@dp.message(F.text == 'Мой профиль', FSM.main_menu_next)
async def get_my_profile(message: types.Message, state: FSMContext):
    # data = requests.get('https://gear.dino-misis.ru/user/profile').json()
    data = s.get('http://127.0.0.1:8000/user/profile').json()
    print(data)
    email = data.get('email')
    name = data.get('name')

    await message.answer(f'Имя : {name} \nПочта: {email}', reply_markup=profile_keyboard)
    await state.set_state(FSM.profile_choice)


@dp.message(F.text == 'Изменить профиль', FSM.profile_choice)
async def change_profile(message: types.Message, state: FSMContext):
    await message.answer(text='Какие данные хотите изменить?', reply_markup=update_profile_keyboard)
    await state.set_state(FSM.change_profile_next)


@dp.message(F.text == 'В главное меню', FSM.profile_choice)
async def redirect_from_profile(message: types.Message, state: FSMContext):
    await message.answer('Главное меню', reply_markup=main_keyboard)
    await state.set_state(FSM.main_menu_next)


@dp.message(F.text.in_({'email', 'имя'}), FSM.change_profile_next)
async def change_profile_email(message: types.Message, state: FSMContext):
    await message.answer(f'Введите {message.text}:',
                         reply_markup=ReplyKeyboardRemove())
    await state.update_data(profile_update_type=message.text)
    await state.set_state(FSM.request_change_profile_next)


@dp.message(FSM.request_change_profile_next)
async def put_change_profile(message: types.Message, state: FSMContext):
    data = await state.get_data()
    profile_update_type = data.get('profile_update_type')
    payload = {'name' if profile_update_type == 'имя' else 'email': message.text}

    user_id = s.get('http://127.0.0.1:8000/user/profile').json().get('id')
    url = f'http://127.0.0.1:8000/user/{user_id}'
    response = s.put(url, json=payload)
    print(payload)
    print(response, str(response.content))

    await message.answer(f'{profile_update_type}: {message.text} - изменения прошли успешно!',
                         reply_markup=main_keyboard)
    await state.set_state(FSM.main_menu_next)




async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
