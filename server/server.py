
import asyncio
import logging
import os
import aiohttp
from lxml import etree
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from random import choice

API_TOKEN = '824051603:AAGl_5lgRtI515dhMB1L63HnItvdsqV-5LU'
PROJECT_NAME = os.getenv('PROJECT_NAME', 'aiogram-example')

# webhook settings
WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = os.environ.get('PORT')

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop)
dp = Dispatcher(bot)


inline_keyboard = types.InlineKeyboardMarkup()
random_button = types.InlineKeyboardButton('Получить случайную цитату', callback_data='refresh')
inline_keyboard.add(random_button)

async def get_random_bash_quote():
    """Downloads bash.im/random page, parses it and returns random quote"""
    bash_url = 'https://bash.im/random'

    async with aiohttp.ClientSession() as session:
        async with session.get(bash_url) as resp:
            html = await resp.text()

    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    quote_tags = tree.xpath('//div[@class="text"]')  # Xpath is a query language for selecting specific tags
    random_quote_tag = choice(quote_tags)
    random_quote = '\n'.join(random_quote_tag.itertext())  # The easiest way to get text inside tag divided by br tags
    return random_quote


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """Handle start command"""
    random_quote = await get_random_bash_quote()
    await message.reply(random_quote, reply_markup=inline_keyboard)


@dp.callback_query_handler(func=lambda cb: True)
async def process_callback_data(callback_query: types.CallbackQuery):
    """Handle all callback data which is being sent to bot"""
    action = callback_query.data

    if action == 'refresh':
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id
        random_quote = await get_random_bash_quote()
        await bot.edit_message_text(random_quote, chat_id, message_id, reply_markup=inline_keyboard)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass


def launch():
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
                  skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)

