from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_category_item, banned_users

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📦Каталог')],
                                     [KeyboardButton(text='⚜️Контакты'), KeyboardButton(text='✏️Написать админу')],
                                     [KeyboardButton(text='/donate'), KeyboardButton(text='/refund')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')


mainadmin=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📦Каталог')],
                                     [KeyboardButton(text='⚜️Контакты'), KeyboardButton(text='✏️Написать админу')],
                                     [KeyboardButton(text='/donate'), KeyboardButton(text='/refund')],
                                     [KeyboardButton(text='👤Админ панель' )]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

adminpanel2 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/writeuser')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

proverka_pokupki = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Проверка оплаты')]],
                            resize_keyboard=True,
                            input_field_placeholder='Выберите пункт меню...')


buy = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить', callback_data='buy_brawl_pass')]])
admin = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Админ', url='https://t.me/klaxxon_oficial')],
                                              [InlineKeyboardButton(text='Канал', url='https://t.me/klaxxon_off')]])
                                                          

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
                                                           request_contact=True)]],
                                 resize_keyboard=True)


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))

    return keyboard.adjust(2).as_markup()

async def banned_userss():
    all_banned_users=await banned_users()
    keyboard = InlineKeyboardBuilder()
    for user in all_banned_users:
        keyboard.add(InlineKeyboardButton(text=user.banned, callback_data=f"bunned_users_{user.id}"))
    return keyboard.adjust(2).as_markup()

async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='main'))
    return keyboard.adjust(2).as_markup()

async def adminpanel():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Забанить', callback_data="banned"), InlineKeyboardButton(text='Разбанить', callback_data="unbanned"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='main'), InlineKeyboardButton(text='Список забаненных', callback_data='bunned_users_spisok'))
    return keyboard.adjust(2).as_markup()

async def mail_and_code():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Ввести свои данные', callback_data="mail"))
    return keyboard.adjust(2).as_markup()

