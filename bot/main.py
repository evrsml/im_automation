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
from keyboard import mode_selector, ModeSelectCallback, pass_approve, change_password, close
from IM_scripts.manual_publication_error.main import start_handpub_error
from IM_scripts.first_answer.main import start_first_answer
from IM_scripts.VDL.main import start_vdl
from IM_scripts.auth.auth import GetAuth
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


'''обработчик на команду /start'''
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if user_check(await bot.get_chat_member(chat_id=GROUP, user_id=message.from_user.id)):
        await bot.send_message(message.from_user.id, text="Выбрать режим автоматизации:", reply_markup=mode_selector())
    else:
        await bot.send_message(message.from_user.id, text='У вас нет доступа')


'''обработчик нового пароля'''
@dp.message(Form.auth, F.text)
async def get_new_password(message: types.Message, state: FSMContext):

    await state.update_data(password=message.text)
    await message.answer(text="Вы уверены, что хотите изменить пароль?", reply_markup=pass_approve())


'''обработка коллбэков для меню выбора режимов автоматизации'''
@dp.callback_query(ModeSelectCallback.filter(F.type == 'mode'))
async def mode_btn_select_action(callback: types.CallbackQuery, callback_data: ModeSelectCallback):

    '''скрипт проверки ошибки публикации'''

    if callback_data.action == 'pub_error':

        '''блок проверки авторизации'''

        auth = GetAuth()
        auth.check_token()

        token = auth.check_token()

        if token:
            result = start_handpub_error(token)
            data = len(result)
            document = FSInputFile('ошибка публикации.txt')
            await bot.send_message(callback.message.chat.id, text='⏳ Процесс пошел...\nЭто может занять некоторое время')
            await bot.send_message(callback.message.chat.id, text=f'✅ Количество инцидентов с ошибкой публикации: {data}')

            if document is not None:
                await bot.send_document(callback.message.chat.id, document)
        else:
            await bot.send_message(callback.message.chat.id, text=f'❌ Проблемы с авторизацией, обновите пароль для аккаунта')

    if callback_data.action == 'auth':
        await bot.send_message(callback.message.chat.id, text='Что сделать?',
                               reply_markup=change_password())

    '''скрипт для проведения первичного ответа'''

    if callback_data.action == 'first_answer':

        '''блок проверки авторизации'''

        auth = GetAuth()
        auth.check_token()

        token = auth.check_token()

        await bot.send_message(callback.message.chat.id, text='⏳ Процесс пошел...\nЭто может занять некоторое время')

        if token:
            result = start_first_answer(token)
            document = FSInputFile('отчет по первичным ответам.txt')
            await bot.send_message(callback.message.chat.id,
                                   text=result)
            if document is not None:
                await bot.send_document(callback.message.chat.id, document)

        else:
            await bot.send_message(callback.message.chat.id,
                               text=f'❌ Проблемы с авторизацией, обновите пароль для аккаунта')

    '''скрпипт для заполнения поля источник ВДЛ ВК в карточке инцидента'''

    if callback_data.action == 'VDL':

        '''блок проверки авторизации'''

        auth = GetAuth()
        auth.check_token()

        token = auth.check_token()

        await bot.send_message(callback.message.chat.id, text='⏳ Процесс пошел...\nЭто может занять некоторое время')

        if token:
            result = start_vdl(token)
            await bot.send_message(callback.message.chat.id,
                                   text=result)
        else:
            await bot.send_message(callback.message.chat.id,
                                   text=f'❌ Проблемы с авторизацией, обновите пароль для аккаунта')

'''обработчик коллбэков для меню авторизации'''
@dp.callback_query(ModeSelectCallback.filter(F.type == 'auth'))
async def auth_management(callback: types.CallbackQuery, callback_data: ModeSelectCallback, state: FSMContext):

    if callback_data.action == 'change_password':

        await state.set_state(Form.auth)
        await bot.send_message(callback.message.chat.id, text='Отправьте новый пароль для пользователя rbintern.03@gmail.com', reply_markup=close())

    if callback_data.action == 'approve':

        await state.set_state(Form.password)
        data = await state.get_data()
        redis = Redis()

        if redis.update_password(new_password=data['password']):
            await bot.send_message(callback.message.chat.id,
                                   text='✅ Пароль успешно обновлен!',
                                   reply_markup=mode_selector())
            await state.clear()

        else:
            await bot.send_message(callback.message.chat.id,
                                   text='❌ Произошла ошибка, попробуйте еще раз')
            await state.clear()

    if callback_data.action == 'close':

        await bot.delete_message(callback.message.chat.id, message_id=callback.message.message_id)
        await state.clear()


    if callback_data.action == 'add_account':

        await bot.send_message(callback.message.chat.id, text="🔜 Функция добавления дополнительного аккаунта пока в разработке", reply_markup=close())

async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())