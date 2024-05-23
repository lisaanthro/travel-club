from aiogram import types


def create_start_keyboard():
    start_itembtn1 = types.KeyboardButton(text='Вход')
    start_itembtn2 = types.KeyboardButton(text='Регистрация')
    # kb = [[itembtn1], [itembtn2]]
    start_keyboard = types.ReplyKeyboardMarkup(keyboard=[[start_itembtn1], [start_itembtn2]],
                                               resize_keyboard=True)

    return start_keyboard


def create_main_keyboard():
    main_itembtn1 = types.KeyboardButton(text='Мой профиль')
    main_itembtn2 = types.KeyboardButton(text='Список пользователей')
    main_itembtn3 = types.KeyboardButton(text='Список снаряжения для аренды')
    main_itembtn4 = types.KeyboardButton(text='История операций для сдачи снаряжения')
    main_itembtn5 = types.KeyboardButton(text='В начало')
    main_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[main_itembtn1], [main_itembtn2], [main_itembtn3], [main_itembtn4]],
        resize_keyboard=True)

    return main_keyboard


def create_profile_keyboard():
    profile_button1 = types.KeyboardButton(text='Изменить профиль')
    profile_button2 = types.KeyboardButton(text='В главное меню')
    profile_keyboard = types.ReplyKeyboardMarkup(keyboard=[[profile_button1], [profile_button2]],
                                                 resize_keyboard=True)

    return profile_keyboard


def create_update_profile_keyboard():
    update_profile_button1 = types.KeyboardButton(text='email')
    update_profile_button2 = types.KeyboardButton(text='имя')
    update_profile_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[update_profile_button1], [update_profile_button2]], resize_keyboard=True)

    return update_profile_keyboard


def create_item_keyboard():
    item_keyboard_button1 = types.KeyboardButton(text='Добавить снаряжение')
    item_keyboard_button2 = types.KeyboardButton(text='Списать снаряжение')
    item_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[item_keyboard_button1], [item_keyboard_button2]], resize_keyboard=True)

    return item_keyboard


def create_item_id_keyboard():
    item_id_keyboard_button1 = types.KeyboardButton(text='Изменить')
    item_id_keyboard_button2 = types.KeyboardButton(text='Посмотреть транзакции')
    item_id_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[item_id_keyboard_button1], [item_id_keyboard_button2]], resize_keyboard=True)

    return item_id_keyboard


def create_update_item_keyboard():
    update_item_button1 = types.KeyboardButton(text='Название')
    update_item_button2 = types.KeyboardButton(text='Инвентарный номер')
    update_item_button3 = types.KeyboardButton(text='Тип')
    update_item_button4 = types.KeyboardButton(text='Состояние')
    update_item_button5 = types.KeyboardButton(text='Цена')
    update_item_button6 = types.KeyboardButton(text='Фото')
    update_item_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[update_item_button1], [update_item_button2], [update_item_button3],
                  [update_item_button4], [update_item_button5], [update_item_button6]], resize_keyboard=True)

    return update_item_keyboard


start_keyboard = create_start_keyboard()
main_keyboard = create_main_keyboard()
profile_keyboard = create_profile_keyboard()
update_profile_keyboard = create_update_profile_keyboard()
item_keyboard = create_item_keyboard()
item_id_keyboard = create_item_id_keyboard()
update_item_keyboard = create_update_item_keyboard()
