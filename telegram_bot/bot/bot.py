import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import ClientSession
import os

from http import HTTPStatus
from s3_script import s3_client as s3, S3_BUCKET_NAME

from config_reader import config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State
from aiogram.types import ReplyKeyboardRemove, ContentType, FSInputFile
from keyboards import *
from aiogram.filters import StateFilter
import requests
import json

import emoji
import datetime

s = requests.session()

BOT_TOKEN = config.bot_token.get_secret_value()

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


# storage = MemoryStorage()

class FSM(StatesGroup):
    auth_next = State()
    sign_in_next = State()
    # sign_in_password_next = State()
    sign_up_next = State()
    # sign_up_name_next = State()
    sign_up_password_next = State()
    main_menu_next = State()

    profile_choice = State()
    change_profile_next = State()
    request_change_profile_next = State()

    item_choice = State()
    item_create = State()
    item_id_choice = State()
    change_item_id = State()
    request_change_item_id = State()

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
    response = s.post(url, json=payload)
    if response.status_code == HTTPStatus.OK:
        token = response.json().get('bearer_token')
        print(token)
        s.headers = {'Authorization': f'Bearer {token}'}
        print('registered')

        await message.answer('Данные приняты', reply_markup=main_keyboard)
        await state.set_state(FSM.main_menu_next)
    else:
        await message.answer(str(response.content))


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
async def change_profile_input(message: types.Message, state: FSMContext):
    await message.answer(f'Введите {message.text}:',
                         reply_markup=ReplyKeyboardRemove())
    await state.update_data(profile_update_type=message.text)
    await state.set_state(FSM.request_change_profile_next)


@dp.message(FSM.request_change_profile_next)
async def request_change_profile(message: types.Message, state: FSMContext):
    data = await state.get_data()
    profile_update_type = data.get('profile_update_type')
    payload = {'name' if profile_update_type == 'имя' else 'email': message.text}

    user_id = s.get('http://127.0.0.1:8000/user/profile').json().get('id')
    url = f'http://127.0.0.1:8000/user/{user_id}'
    response = s.put(url, json=payload)
    print(payload)

    await message.answer(f'{profile_update_type}: {message.text} - изменения прошли успешно!',
                         reply_markup=main_keyboard)
    await state.set_state(FSM.main_menu_next)


@dp.message(F.text == 'Список снаряжения для аренды', FSM.main_menu_next)
async def get_all_items(message: types.Message, state: FSMContext):
    url = 'http://127.0.0.1:8000/item'
    response = s.get(url)
    message_text = "Список снаряжения:\n\n"

    for item in response.json():
        item_text = f"/{item.get('id')}\\ {item.get('name')}\\ *{item.get('type')}*\\ {item.get('price')} руб\n"
        message_text += item_text.replace('.', r'\.') + '\n'

    # builder = InlineKeyboardBuilder()
    # builder.row(types.InlineKeyboardButton(text=city, url=link))
    # await message.answer('Перейдите по ссылке ниже:', reply_markup=builder.as_markup())
    await message.answer(text = emoji.emojize(":tent:") + message_text, parse_mode="MarkdownV2", reply_markup=item_keyboard)
    await state.set_state(FSM.item_choice)


@dp.message(F.text.startswith('/'), FSM.item_choice)
async def get_item_by_id(message: types.Message, state: FSMContext):
    item_id = message.text.strip('/')
    url = f'http://127.0.0.1:8000/item/{item_id}'

    response = s.get(url)
    item = response.json()
    print(item)
    item_text = f"{item.get('name')}\n{item.get('inventary_id')}\n{item.get('type')}\n" \
                f"{item.get('condition')}\n{item.get('price')}"

    try:
        file_name = f"{item_id}.jpg"
        file_path = f"{file_name}"  # Temporary local path to save the file

        # Download photo from S3
        s3.download_file(S3_BUCKET_NAME, file_name, file_path)

        # Send photo to user
        print('photo')
        image_from_pc = FSInputFile(file_name)
        result = await message.answer_photo(
            image_from_pc,
            caption=item_text,
            reply_markup=item_id_keyboard
        )
        # TODO: add proper file path
        os.remove(file_path)
    except Exception as e:
        await message.answer(item_text, reply_markup=item_id_keyboard)

    await state.update_data(current_item_id=item_id)
    await state.set_state(FSM.item_id_choice)

@dp.message(F.text == 'Взять в аренду', FSM.item_id_choice)
async def change_item_by_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item_id = int(data.get('current_item_id'))
    await message.answer(text='Введите через пробел стоимость залога и планируемую дату возврата в формате yyyy.mm.dd', reply_markup=ReplyKeyboardRemove())
    await state.update_data(current_item_id=item_id)
    await state.set_state(FSM.rent_next)

@dp.message(FSM.rent_next)
async def create_transaction_by_id(message: types.Message, state: FSMContext):
    url = 'http://127.0.0.1:8000/transaction/create/rent'
    str_pledge, planned_date = message.text.split()
    year, month, day = map(int, planned_date.split('.'))
    end_date = datetime.date(year, month, day)
    str_end_date = str(end_date)
    today = datetime.date.today()
    str_today = str(today)

    data = await state.get_data()
    item_id = int(data.get('current_item_id'))

    pledge = float(str_pledge)
    payload = {'item_id': item_id, 'pledge': pledge, 'start_date': str_today, 'end_date': str_end_date}
    print(payload)
    response = s.post(url, json=payload)

    if response.status_code == HTTPStatus.OK:
        print(response.json())
        await message.answer('Снаряжение забронировано за Вами', reply_markup=main_keyboard)
        await state.set_state(FSM.main_menu_next)
    else:
        print(response.json())
        await message.answer(str(response.content))



@dp.message(F.text == 'Изменить', FSM.item_id_choice)
async def change_item_by_id(message: types.Message, state: FSMContext):
    await message.answer(text='Какие данные хотите изменить?', reply_markup=update_item_keyboard)
    await state.set_state(FSM.change_item_id)


@dp.message(F.text.in_({'Название', 'Инвентарный номер', 'Тип', 'Состояние', 'Цена'}), FSM.change_item_id)
async def change_item_by_id_input(message: types.Message, state: FSMContext):
    await message.answer(f'Введите {message.text}:',
                         reply_markup=ReplyKeyboardRemove())
    await state.update_data(item_update_type=message.text)
    await state.set_state(FSM.request_change_item_id)


@dp.message(F.text == 'Фото', FSM.change_item_id)
async def change_item_photo_input(message: types.Message, state: FSMContext):
    await message.answer('Отправьте сюда фото, которое хотите поставить')
    await state.set_state(FSM.request_change_item_id)


@dp.message(F.content_type == 'photo', FSM.request_change_item_id)
async def request_change_item_photo_by_id(message: types.Message, state: FSMContext):
    photo = message.photo[-1]  # Get the highest resolution photo
    data = await state.get_data()
    item_id = data.get('current_item_id')

    # Download the photo
    file_info = await bot.get_file(photo.file_id)
    file_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}'

    async with ClientSession() as session:
        async with session.get(file_url) as resp:
            if resp.status == 200:
                file_data = await resp.read()
                file_name = f"{item_id}.jpg"

                # Save the photo locally
                with open(file_name, 'wb') as f:
                    f.write(file_data)

                # Upload to S3
                try:
                    s3.upload_file(file_name, S3_BUCKET_NAME, file_name)
                    await message.reply("Фото обновлено!", reply_markup=main_keyboard)

                    # Delete the local file
                    os.remove(file_name)
                    await state.set_state(FSM.main_menu_next)
                except Exception as e:
                    await message.reply("Failed to upload photo to S3")
            else:
                await message.reply("Failed to download photo")


@dp.message(FSM.request_change_item_id)
async def request_change_item_by_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item_id = data.get('current_item_id')
    item_update_type = data.get('item_update_type')

    item_property = 'name'
    if item_update_type == 'Инвентарный номер':
        item_property = 'inventary_id'
    elif item_update_type == 'Тип':
        item_property = 'type'
    elif item_update_type == 'Состояние':
        item_property = 'condition'
    else:
        item_property = 'price'

    payload = {item_property: message.text}
    url = f'http://127.0.0.1:8000/item/{item_id}'
    response = s.put(url, json=payload)

    print(response)
    print(response.json())
    await message.answer(f'{item_update_type}: {message.text} - изменения прошли успешно!',
                         reply_markup=main_keyboard)
    await state.set_state(FSM.main_menu_next)


@dp.message(F.text == 'Посмотреть транзакции', FSM.item_id_choice)
async def get_transactions_by_item_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item_id = data.get('current_item_id')

    url = f'http://127.0.0.1:8000/transaction/item/{item_id}'
    response = s.get(url)
    message_text = "Список транзакций:\n"

    for transaction in response.json():
        item_text = f"/{transaction.get('id')}\n{transaction.get('user_id')}\n{transaction.get('type')}\n{transaction.get('cost')} руб\n" \
                    f"{transaction.get('start_date')}\n{'Не завершена' if transaction.get('final_end_date') is None else 'Завершена'}"
        message_text += item_text + '\n'

    await message.answer(message_text, reply_markup=main_keyboard)
    await state.set_state(FSM.main_menu_next)


@dp.message(F.text == 'Добавить снаряжение', FSM.item_choice)
async def item_create(message: types.Message, state: FSMContext):
    answer_text = '''Введите каждое значение в отдельной строке
    Название
    Инвентарный номер
    Тип снаряжения
    Состояние снаряжения
    Цена (руб)'''
    await message.answer(answer_text)
    await state.set_state(FSM.item_create)


@dp.message(FSM.item_create)
async def request_item_create(message: types.Message, state: FSMContext):
    print(message.text)
    data_input = message.text

    # TODO: validate that input consists of 5 values, separated by '\n', inventary_id and price are int
    name, inventary_id, item_type, condition, price = message.text.split('\n')
    inventary_id = int(inventary_id)
    price = int(price)

    payload = {"name": name,
               "inventary_id": inventary_id,
               "type": item_type,
               "condition": condition,
               "price": price,
               "image": "string"}
    url = 'http://127.0.0.1:8000/item/create'
    response = s.post(url, json=payload)
    print(payload, response, str(response.content))
    print(response.json())

    await message.answer(f'Снаряжение {name} было добавлено', reply_markup=main_keyboard)
    await state.set_state(FSM.main_menu_next)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
