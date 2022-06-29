from os import curdir
import sqlite3 as sq
from create_bot import dp, bot

def sql_start():
    global base, cur
    base = sq.connect('svit_kartyn_db.db')
    cur = base.cursor()
    if base:
        print('База даних підключилася успішно!')
    base.execute('CREATE TABLE IF NOT EXISTS paintings(img TEXT, title TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO paintings VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM paintings').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОпис: {ret[2]}\nЦіна: {ret[-1]}')

async def sql_read2():
    return cur.execute('SELECT * FROM paintings').fetchall()

async def sql_delete_command(data):
    cur.execute('DELETE FROM paintings WHERE title == ?', (data,))
    base.commit()