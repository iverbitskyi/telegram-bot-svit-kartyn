from ast import Lambda
from cmd import IDENTCHARS
from typing import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher 
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data_base.sqlite_db import sql_add_command, sql_delete_command

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    title = State()
    description = State()
    price = State()

# отримуємо ID поточного модератора
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Ви у режимі адміністратора! Створіть карточку товару', reply_markup=admin_kb.kb_admin_add)
    await message.delete()

# Початок діалогу і загрузка нового пункту меню
async def cm_start(message : types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Завантажте фото', reply_markup=admin_kb.kb_admin_cancel)

# вихід з стану
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Створення карточки товару скасовано!', reply_markup=admin_kb.kb_admin_back)

# Лапаємо першу відповідь і записуємо в словник
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Ведіть назву', reply_markup=admin_kb.kb_admin_cancel)

# Лапаємо другу відповідь
async def load_title(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply("Введіть опис")

# Лапаємо третю відповідь
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply("Введіть ціну")

# Лапаємо четветру відповідь
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await sqlite_db.sql_add_command(state)
        await state.finish()
        await message.reply('Новий товар успішно створений!', reply_markup=admin_kb.kb_admin_back)

# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} видалено!', show_alert=True)

# @dp.message_handler(commands='видалити')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОпис: {ret[2]}\nЦіна: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Видалити {ret[1]}', callback_data=f'del {ret[1]}')))

# реєструємо холдери
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['завантажити'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='скасувати')
    dp.register_message_handler(cancel_handler, Text(equals='скасувати', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_title, state=FSMAdmin.title)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, commands='видалити')