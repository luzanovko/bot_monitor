from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher
from aiogram.types import InputFile

from config import TOKEN
import keyboard as kb
import requests
import os
import time
from requests.auth import HTTPDigestAuth

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


        
##Body bot

@dp.callback_query_handler(lambda c: c.data == 'camera1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if os.path.isfile('foto.png'):
         os.remove('foto.png')
    get_snap(81)
    if os.path.isfile('foto.png'):
        photo = open ('foto.png', 'rb')    
        await bot.send_photo(callback_query.from_user.id, photo=photo)
    else: await bot.send_message(callback_query.from_user.id, "Ошибка загрузки изображения c камеры.\nПопробуй позже или другую команду /help")
     
@dp.callback_query_handler(lambda c: c.data == 'camera2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if os.path.isfile('foto.png'):
         os.remove('foto.png')
    get_snap(82)
    if os.path.isfile('foto.png'):
        photo = open ('foto.png', 'rb')    
        await bot.send_photo(callback_query.from_user.id, photo=photo)
    else: await bot.send_message(callback_query.from_user.id, "Ошибка загрузки изображения c камеры.\nПопробуй позже или другую команду /help")
    

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    comproxy_keyboard = types.InlineKeyboardMarkup()
    call_button_comproxy_old = types.InlineKeyboardButton(text="Камера 1", callback_data="camera1")
    call_button_comproxy_new = types.InlineKeyboardButton(text="Камера 2", callback_data="camera2")
    
    comproxy_keyboard.add(call_button_comproxy_old, call_button_comproxy_new)
    await message.answer("Доброго дня " + message.from_user.first_name + ", Я бот-инженер\n Какую камеру показать ..", reply_markup=comproxy_keyboard)



help_message = text(
    "Бот УФК по Самарской области.",
    "Доступные команды:\n",
    "/start - приветствие",
    "/cam1 - камера-1",
    "/cam2 - камера-2",
    "/ping - ping 1.1.1.1",
    sep="\n"
)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(help_message)


def get_snap(port):
    
    #user = 'admin'
    #password = ''
    #url = 'http://admin@192.168.2.105:82/dms'
    #response = requests.get(url)
    #print (url)
    #print (response.status_code)
    #if response.status_code == 200:
    #    with open('foto.png', 'wb') as f:
    #        f.write(response.content)
    link = f'http://192.168.2.105:{port}/dms'
    s = requests.Session()
    s.auth = ('admin', '')
    photo = s.get(link)
#    print(f'Status Code: {r.status_code}')
    if photo.status_code == 200:
        with open('foto.png', 'wb') as f:
            f.write(photo.content)
            f.close()
    #else
    
@dp.message_handler(commands=['cam1'])
async def process_cam1_command(message: types.Message):
     if os.path.isfile('foto.png'):
         os.remove('foto.png')
     get_snap(81)
     photo = open ('foto.png', 'rb')    
     #command = 'curl -o /bot/foto.png http://admin@192.168.2.105:81/dms'
     await bot.send_photo(chat_id=message.chat.id, photo=photo)
     
@dp.message_handler(commands=['cam2'])
async def process_cam1_command(message: types.Message):
     if os.path.isfile('foto.png'):
         os.remove('foto.png')
     get_snap(82)
     photo = open ('foto.png', 'rb')    
     #command = 'curl -o /bot/foto.png http://admin@192.168.2.105:81/dms'
     await bot.send_photo(chat_id=message.chat.id, photo=photo)
     

    
@dp.message_handler(commands=['ping'])
async def process_cam1_command(message: types.Message):

    hostname = "1.1.1.1"
    response = os.system('ping -c 2 {} > /dev/null'.format(hostname))
    if response == 0:
        #print(hostname + ' is up!')
        await bot.send_message(message.from_user.id, hostname + ' is up!')
    else:
        #print(hostname + ' is down!')
        await bot.send_message(message.from_user.id, hostname + ' is down!')
    
@dp.message_handler()
async def unknown_message(message: types.Message):
    """Ответ на любое неожидаемое сообщение"""
    await message.answer("Ничего не понятно, но очень интересно.\nПопробуй команду /start")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

