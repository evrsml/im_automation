from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import types


load_dotenv()

TOKEN = os.environ.get('TOKEN')
GROUP = os.environ.get('GROUP')

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)
router = Router()

'''класс состояний'''
class Form(StatesGroup):
    mode = State()

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
        await bot.send_message(message.from_user.id, text="Выбрать эксперта", reply_markup=keyboard_supermen())
    else:
        await bot.send_message(message.from_user.id, text='У вас нет доступа')