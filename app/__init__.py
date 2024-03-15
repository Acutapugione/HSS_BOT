import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from dotenv import load_dotenv
load_dotenv()

from app.utils.api_worker import API_Worker
from . enums import Settings

router = Router()

from . config import Config 
from . menu import Auth

bot = Bot(token=Config.TOKEN, parse_mode=ParseMode.HTML)
api_worker = API_Worker()


async def background_on_start() -> None:
    """background task which is created when bot starts"""
    while True:
        await asyncio.sleep(5)
        print("Hello World!")
        messages = await api_worker.get_messages(lambda x: x.get("is_sended")==False and x.get("telegram_id") is not None)
        if messages:
            for message in messages:
                await bot.send_message(message.get("telegram_id"), message.get("text"))
                await api_worker.mark_as_read_message(message)

async def on_bot_start_up(dispatcher: Dispatcher) -> None:
    """List of actions which should be done before bot start"""
    asyncio.create_task(background_on_start())  # creates background task

async def main():
    
    dp = Dispatcher()
    dp.startup.register(on_bot_start_up)
    dp.include_router(router)
    await dp.start_polling(bot)