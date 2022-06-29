from aiogram import types, Dispatcher 
from create_bot import dp, bot
from keyboards import kb_client_start, kb_client_menu, kb_client_shops, kb_client_manager
from data_base import sqlite_db

async def command_start(message : types.Message):
    try:
        mess = f"Привіт, <b>{message.from_user.first_name}</b>. Вас вітає Svit kartyn Bot.\n\nТут Ви можете отримати інформацію про наші магазини, товари та зв'язатися з нами для замовлення товару\n\nДля спілкування з нашим ботом, ви можете використати наступні команди: \n/start \n/help"
        await bot.send_message(message.from_user.id, mess, parse_mode='html', reply_markup=kb_client_start)
    except:
        await message.reply('Спілкування з ботом можливе через приватні повідомлення, \nБудь ласка, напишіть йому: @svit_kartyn_bot')

async def command_menu(message : types.Message):
    await bot.send_message(message.from_user.id, "Вітаємо в меню!\n\nБудь ласка оберіть пункт, щоб перейти далі", parse_mode='html', reply_markup=kb_client_menu)

async def command_shops(message : types.Message):
    await bot.send_message(message.from_user.id, "Поки ми маємо лише онлайн магазини, згодом відкриємо також офлайн точки", parse_mode='html', reply_markup=kb_client_start)
    await bot.send_message(message.from_user.id, "Переходьте у наш Instagram чи OLX", parse_mode='html', reply_markup=kb_client_shops)

async def command_painting(message : types.Message):
    await bot.send_message(message.from_user.id, "Тут ви можете побачити створені нами картини", parse_mode='html', reply_markup=kb_client_start)
    await sqlite_db.sql_read(message)

async def command_order(message : types.Message):
    await bot.send_message(message.from_user.id, "Для створення картини під замовлення, будь ласка, напишіть нам, що ви хочете бачити та надішліть приблизний приклад картини", parse_mode='html', reply_markup=kb_client_start)
    await bot.send_message(message.from_user.id, "Напишіть нашому менеджеру, або залиште свої контакти, ми зв'яжемося з вами", parse_mode='html', reply_markup=kb_client_manager)

async def command_chat_manager(message : types.Message):
    await bot.send_message(message.from_user.id, "Це наш менеджер: @vverbitskyi.\nЗадайте йому будь-яке питання, що вас цікавить", parse_mode='html', reply_markup=kb_client_start)

# реєструємо холдери
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_menu, commands=['меню'])
    dp.register_message_handler(command_shops, commands=['наші_магазини'])
    dp.register_message_handler(command_painting, commands=['наші_товари'])
    dp.register_message_handler(command_order, commands=['картина_під_замовлення'])
    dp.register_message_handler(command_chat_manager, commands=['чат_з_менеджером'])

