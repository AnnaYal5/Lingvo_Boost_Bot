import asyncio
import time
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import os
import random
import tkinter as tk
import json
# import bot_funcs
import random
with (open('abbreviations.json', 'r', encoding='utf-8') as f):
    list_of_keys_a = []
    jsf_a = json.load(f)  # dict
    for i in jsf_a.keys():
        list_of_keys_a.append(i)
    jsfa_new = jsf_a
    list_of_keys_a_new = list_of_keys_a

with (open('idioms.json', 'r', encoding='utf-8') as f):
    list_of_keys_i = []
    jsf_i = json.load(f)  # dict
    for i in jsf_i.keys():
        list_of_keys_i.append(i)
    jsfi_new = jsf_i
    list_of_keys_i_new = list_of_keys_i

def getnow():
    randfile = random.randint(0, 1)
    if randfile == 0:
        rkey = random.choice(list_of_keys_i_new)
        rval = jsfi_new.pop(str(rkey))
        if rkey in list_of_keys_i_new:
            list_of_keys_i_new.remove(rkey)
        return str(rval).replace(";", '.')
    elif randfile == 1:
        rkey = random.choice(list_of_keys_a_new)
        rval = jsfa_new.pop(str(rkey))
        if rkey in list_of_keys_a_new:
            list_of_keys_a_new.remove(rkey)
        return str(rval) + '.'



load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
Buttons_keyboard = ReplyKeyboardBuilder()
Buttons = ['set timer', 'get now']
TIMER = ['5 sec', "10 min", "30 min", '1hrs', '2hrs', '3hrs', 'back', 'turn off']
Buttons_keyboard.add(*[types.KeyboardButton(text=i) for i in Buttons])
Buttons_keyboard.adjust(2)


timer_keyboard = ReplyKeyboardBuilder()
timer_keyboard.add(*[types.KeyboardButton(text=i) for i in TIMER])
timer_keyboard.adjust(2)
@dp.message(Command(commands = ['start']))
async def send_message(message:types.message):
    await message.answer('Hello! choose command', reply_markup=Buttons_keyboard.as_markup(resize_keyboard=True))

@dp.message(lambda message: message.text in Buttons)
async def choose_option(message: types.message):
    userid = message.from_user.id
    if message.text == 'get now':

        await message.answer(getnow())
    elif message.text == "set timer":
        await message.answer("please choose time", reply_markup=timer_keyboard.as_markup(resize_keyboard=True))

user_timers = {}

@dp.message(lambda message: message.text in TIMER)
async def set_timer(message: types.Message):
    global timer
    user_id = message.from_user.id

    times = {
        '5 sec': 5,
        '10 min': 10 * 60,
        '30 min': 30 * 60,
        '1hrs': 60 * 60,
        '2hrs': 2 * 60 * 60,
        '3hrs': 3 * 60 * 60
    }

    if message.text in times:
        delay = times[message.text]
        if user_id in user_timers and not user_timers[user_id].done():
            user_timers[user_id].cancel()
        await message.answer(f'Timer set for {message.text}.')
        user_timers[user_id] = asyncio.create_task(timer_task(message, delay))
    elif message.text == 'turn off':
        if user_id in user_timers and not user_timers[user_id].done():
            user_timers[user_id].cancel()
    elif message.text == 'back':
        await message.answer('Choose command', reply_markup=Buttons_keyboard.as_markup(resize_keyboard=True))




async def timer_task(message: types.Message, delay: int):
    while True:
        try:
            await asyncio.sleep(delay)
            message_ = getnow()
            await message.answer(message_)
        except asyncio.CancelledError:
            await message.answer('Timer was cancelled.')
            break


if __name__ == "__main__":
    dp.run_polling(bot)