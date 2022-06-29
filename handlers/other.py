from aiogram import types, Dispatcher
from create_bot import dp
import json, string

async def censor_checker(message : types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('censor.json')))) != set():
        await message.reply('Нецензурна лексика заборонена!')
        await message.delete()

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(censor_checker)
