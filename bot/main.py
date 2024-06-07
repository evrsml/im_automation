import asyncio
import logging

from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import types
from aiogram.types import FSInputFile
from keyboard import mode_selector, ModeSelectCallback

from IM_scripts.manual_publication_error.main import start_handpub_error


logging.basicConfig(level=logging.INFO)

load_dotenv()

TOKEN = os.environ.get('TOKEN')
GROUP = os.environ.get('GROUP')

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)


'''класс состояний'''
class Form(StatesGroup):
    mode = State()
    auth = State()

'''авторизация пользователя'''
def user_check(chat_member):
    if dict(chat_member)['status'] != 'left' and dict(chat_member)['status'] != 'kicked':
        return True
    else:
        return False

'''хэндлер на команду /start'''

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if user_check(await bot.get_chat_member(chat_id=GROUP, user_id=message.from_user.id)):
        await bot.send_message(message.from_user.id, text="Выбрать режим автоматизации:", reply_markup=mode_selector())
    else:
        await bot.send_message(message.from_user.id, text='У вас нет доступа')

@dp.callback_query(ModeSelectCallback.filter(F.type == 'mode'))
async def expert_btn_select_action(callback: types.CallbackQuery, callback_data: ModeSelectCallback, state: FSMContext):

    if callback_data.action == 'pub_error':
        result = start_handpub_error()
        data = len(result)
        document = FSInputFile('ошибка публикации.txt')
        await bot.send_message(callback.message.chat.id, text=f'Количество инцидентов с ошибкой публикации: {data}')
        await bot.send_document(callback.message.chat.id, document)


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())