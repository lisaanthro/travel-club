import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import StatesGroup

from config_reader import config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State
from keyboards import start_keyboard, main_keyboard
from aiogram.filters import StateFilter
import requests
import json

bot = Bot(token = config.bot_token.get_secret_value())
dp = Dispatcher()
#storage = MemoryStorage()

class FSM(StatesGroup):
    auth_next = State()
    sign_in_next = State()
    #sign_in_password_next = State()
    sign_up_next = State()
    #sign_up_name_next = State()
    sign_up_password_next = State()
    main_menu_next = State()
    change_profile_next = State()
    get_item_info_for_rent_next = State()
    get_item_info_for_return_next = State()
    rent_next = State()
    return_next = State()



@dp.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('Привет, я - бот-помощник туристического клуба университета МИСИС. Помогаю арендовывать снаряжение. \nДля работы со мной необходимо войти в аккаунт или зарегистрироваться.\nДо встречи в аккаунте!', reply_markup=start_keyboard)
    await state.set_state(FSM.auth_next)

@dp.message(F.text == "Вход", FSM.auth_next)
async def sigh_in(message: types.Message, state: FSMContext):
    await message.answer('Введите почту и пароль через пробел')
    await state.set_state(FSM.sign_in_next)

@dp.message(F.text == "Регистрация", FSM.auth_next)
async def sigh_up(message: types.Message, state: FSMContext):
    await message.answer('Введите почту, имя и пароль через пробелы в соответствующем порядке')
    await state.set_state(FSM.sign_up_next)

@dp.message(F.text.contains('@'), FSM.sign_up_next)
async def post_mail_name_password(message: types.Message, state: FSMContext):
    url = 'https://gear.dino-misis.ru/user/register'
    email, name, password = message.text.split()
    payload = {'email': email, 'name': name, 'password': password}
    token = requests.post(url, json=payload)
    await message.answer('Данные приняты', reply_markup=main_keyboard, headers={'Registration': f'{token}'})
    await state.set_state(FSM.main_menu_next)

@dp.message(F.text.contains('@'), FSM.sign_in_next)
async def post_mail_password(message: types.Message, state: FSMContext):
    url = 'https://gear.dino-misis.ru/user/login'
    email, password = message.text.split()
    payload = {'email': email, 'password': password}
    token = requests.post(url, json=payload)
    await message.answer('Данные приняты', reply_markup=main_keyboard, headers={'Authorization': f'{token}'})
    await state.set_state(FSM.main_menu_next)

@dp.message(F.text == 'Мой профиль', FSM.main_menu_next)
async def get_my_profile(message: types.Message, state: FSMContext):
    data = requests.get('https://gear.dino-misis.ru/user/profile').json()
    email = data.get('email')
    name = data.get('name')
    await message.answer(f'Имя : {name}, \nПочта: {email}')
    await state.set_state(FSM.change_profile_next)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())