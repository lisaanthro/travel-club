from aiogram import types


start_itembtn1 = types.KeyboardButton(text = 'Вход')
start_itembtn2 = types.KeyboardButton(text = 'Регистрация')
#kb = [[itembtn1], [itembtn2]]
start_keyboard = types.ReplyKeyboardMarkup(keyboard=[[start_itembtn1], [start_itembtn2]], resize_keyboard=True)


main_itembtn1 = types.KeyboardButton(text = 'Мой профиль')
main_itembtn2 = types.KeyboardButton(text = 'Список пользователей')
main_itembtn3 = types.KeyboardButton(text = 'Список снаряжения для аренды')
main_itembtn4 = types.KeyboardButton(text = 'Историю операций для сдачи снаряжения')
main_itembtn5 =  types.KeyboardButton(text = 'В начало')
main_keyboard = types.ReplyKeyboardMarkup(keyboard=[[main_itembtn1], [main_itembtn2], [main_itembtn3], [main_itembtn4]], resize_keyboard=True)

