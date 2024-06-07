# -*- coding: utf-8 -*-
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from typing import Optional


'''класс для обработки поведения колбэков клавиатуры'''
class ModeSelectCallback(CallbackData, prefix='mode'):

    type: str
    action: Optional[str] = None


'''клавитура выбора режимов работы'''
def mode_selector():
    builder = InlineKeyboardBuilder()
    builder.button(text="Первичный ответ",
                   callback_data=ModeSelectCallback(type="mode", action="first_answer"))
    builder.button(text="Ошибка публикации",
                   callback_data=ModeSelectCallback(type="mode", action="pub_error"))
    builder.button(text="ВДЛ",
                   callback_data=ModeSelectCallback(type="mode", action="VDL"))
    builder.button(text="Аккаунты",
                   callback_data=ModeSelectCallback(type="mode", action="auth"))
    builder.adjust(1)
    return builder.as_markup()

def change_password():
    builder = InlineKeyboardBuilder()
    builder.button(text="Обновить пароль",
                   callback_data=ModeSelectCallback(type="auth", action="change_password"))
    builder.button(text="Добавить аккаунт",
                   callback_data=ModeSelectCallback(type="auth", action="add_account"))
    builder.button(text="Закрыть меню",
                   callback_data=ModeSelectCallback(type="auth", action="close"))
    builder.adjust(1)
    return builder.as_markup()

def pass_approve():
    builder = InlineKeyboardBuilder()
    builder.button(text="Да, сменить пароль",
                   callback_data=ModeSelectCallback(type="auth", action="approve"))
    builder.button(text="Нет, оставить старый пароль",
                   callback_data=ModeSelectCallback(type="auth", action="cancel"))
    builder.adjust(1)
    return builder.as_markup()