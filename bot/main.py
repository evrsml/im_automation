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
from keyboard import mode_selector, ModeSelectCallback, pass_approve, change_password
from IM_scripts.manual_publication_error.main import start_handpub_error
from redis_conf.config import RedisCheck as Redis

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
    password = State()

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

@dp.message(Form.auth, F.text)
async def get_new_password(message: types.Message, state: FSMContext):

    await state.update_data(password=message.text)
    await message.answer(text="Вы уверены, что хотите изменить пароль?", reply_markup=pass_approve())

@dp.callback_query(ModeSelectCallback.filter(F.type == 'mode'))
async def expert_btn_select_action(callback: types.CallbackQuery, callback_data: ModeSelectCallback):

    if callback_data.action == 'pub_error':

        result = start_handpub_error()

        if result:
            data = len(result)
            document = FSInputFile('ошибка публикации.txt')
            await bot.send_message(callback.message.chat.id, text='⏳ Процесс пошел...\nЭто может занять некоторое время')
            await bot.send_message(callback.message.chat.id, text=f'✅ Количество инцидентов с ошибкой публикации: {data}')
            await bot.send_document(callback.message.chat.id, document)
        else:
            await bot.send_message(callback.message.chat.id, text=f'❌ Проблемы с авторизацией, обновите пароль для аккаунта')

    if callback_data.action == 'auth':
        await bot.send_message(callback.message.chat.id, text='Что сделать?',
                               reply_markup=change_password())

@dp.callback_query(ModeSelectCallback.filter(F.type == 'auth'))
async def auth_management(callback: types.CallbackQuery, callback_data: ModeSelectCallback, state: FSMContext):

    if callback_data.action == 'change_password':

        await state.set_state(Form.auth)
        await bot.send_message(callback.message.chat.id, text='Отправьте новый пароль для пользователя rbintern.03@gmail.com')

    if callback_data.action == 'approve':

        await state.set_state(Form.password)
        data = await state.get_data()
        redis = Redis()

        if redis.update_password(new_password=data['password']):
            await bot.send_message(callback.message.chat.id,
                                   text='✅ Пароль успешно обновлен!\nНеобходимо перезапустить бота',
                                   reply_markup=mode_selector())
            await state.clear()

        else:
            await bot.send_message(callback.message.chat.id,
                                   text='❌ Произошла ошибка, попробуйте еще раз')
            await state.clear()

    if callback_data.action == 'close':

            await bot.delete_message(callback.message.chat.id, message_id=callback.message.message_id)

async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())