import logging
import os

from aiogram import Bot, types, md
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '824051603:AAGl_5lgRtI515dhMB1L63HnItvdsqV-5LU'
PROJECT_NAME = os.getenv('PROJECT_NAME', 'aiogram-example')


WEBHOOK_HOST = 'https://english-telegram-bot.herokuapp.com'  # name your app
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
inline_keyboard = InlineKeyboardMarkup()
random_button = types.InlineKeyboardButton('Получить случайную цитату')
inline_keyboard.add(random_button)


@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    # await bot.send_message(
    #     message.chat.id,
    #     f'Приветствую! Это демонтрационный бот\n'
    #     f'Подробная информация на '
    #     f'{md.hlink("github", "https://github.com/deploy-your-bot-everywhere/heroku")}',
    #     parse_mode=types.ParseMode.HTML,
    #     disable_web_page_preview=True)
    await message.reply("Приветствую! Это демонтрационный бот\n", reply_markup=inline_keyboard)


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass


def launch():
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=WEBAPP_HOST, port=WEBAPP_PORT)
