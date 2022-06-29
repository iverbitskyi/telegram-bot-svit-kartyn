from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_add = KeyboardButton('/завантажити')
button_cancel = KeyboardButton('/скасувати')
button_delete = KeyboardButton('/видалити')
button_back = KeyboardButton('/меню')

kb_admin_add = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin_back = ReplyKeyboardMarkup(resize_keyboard=True)


kb_admin_add.add(button_add).add(button_delete)
kb_admin_cancel.add(button_cancel)
kb_admin_back.add(button_add).add(button_delete).add(button_back)