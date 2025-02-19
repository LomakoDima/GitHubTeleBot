import os
import aiohttp
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from config import *




bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Привет! Отправь мне имя пользователя GitHub, и я покажу информацию о нем.")

@dp.message()
async def get_github_user(message: Message):
    username = message.text.strip()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{GITHUB_API_URL}/users/{username}") as response:
            if response.status == 200:
                data = await response.json()
                user_info = (f"👤 Пользователь: {data['login']}\n"
                             f"🔗 Профиль: {data['html_url']}\n"
                             f"📜 Репозитории: {data['public_repos']}\n"
                             f"👥 Подписчики: {data['followers']}\n"
                             f"🌟 Подписки: {data['following']}")
                await message.reply(user_info)
            else:
                await message.reply("Пользователь не найден.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())