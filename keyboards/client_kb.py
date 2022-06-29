from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

b1 = KeyboardButton('/меню')
b2 = KeyboardButton('/наші_магазини')
b3 = KeyboardButton('/наші_товари')
b4 = KeyboardButton('/картина_під_замовлення')
b5 = KeyboardButton('/чат_з_менеджером')
b6 = KeyboardButton('/help')
b7 = InlineKeyboardButton('Instagram', url="https://www.instagram.com/svit.kartyn/")
b8 = InlineKeyboardButton('OLX', url="https://www.olx.ua/uk/list/user/Mwq0P/")
b9 = InlineKeyboardButton("Написати менеджеру", url="https://t.me/vverbitskyi")

kb_client_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_menu = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_shops = InlineKeyboardMarkup()
kb_client_manager = InlineKeyboardMarkup()

kb_client_start.add(b1)
kb_client_menu.add(b2).add(b3).add(b4).add(b5).add(b6)
kb_client_shops.row(b7, b8)
kb_client_manager.add(b9)