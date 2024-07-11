import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode
from aiogram.utils import markdown
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
openai_client = OpenAI()

chatting = False

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer("use '/chatgpt' and say anything to talk to ChatGPT.")

@dp.message(Command("chatgpt"))
async def handle_chatgpt(message: types.Message):
    global chatting
    chatting = True
    await message.answer("send anything to chat with ChatGPT.")

@dp.message(F.text)
async def handle_message(message: types.Message):
    if chatting:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.answer(response.choices[0].message.content.strip())

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())