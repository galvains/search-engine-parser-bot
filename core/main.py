import asyncio
import time

from aiogram import Dispatcher, types, Bot
from aiogram.filters import CommandObject
from aiogram.filters.command import Command

from async_model import gather_data
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer(f"Hello, {message.from_user.first_name}!😀\n"
                         f"I'm a bot for finding the location of a product card on the Wildberries store page.\n"
                         f"Write the /help command for more information.")


@dp.message(Command('help'))
async def start_command(message: types.Message):
    await message.answer(f'Commands:\n<b>/parse</b> "product name" "article number"\n\n'
                         f'For example: "/parse чайник 160512168"', parse_mode='HTML')


@dp.message(Command('parse'))
async def data_collection(message: types.Message, command: CommandObject):
    try:
        arguments = command.args.split(' ')
        start_time = time.time()
        await gather_data(arguments[0], int(arguments[1]), message, start_time)
    except IndexError:
        await message.reply('Please enter ALL arguments')
    except AttributeError:
        await message.reply('Please enter the arguments')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
