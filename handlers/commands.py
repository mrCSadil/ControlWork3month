from aiogram import types , Dispatcher
import os
from config import bot

async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Hello {message.from_user.first_name}!",)

async def info_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Hello i am sails bot and you can choose from my store everything you want to buy \n and then i will made your offer")



def register_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler , commands="start")
    dp.register_message_handler(info_handler , commands="info")