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
                   callback_data=ModeSelectCallback(type="mode", action="first_answer"))
    builder.button(text="ВДЛ",
                   callback_data=ModeSelectCallback(type="mode", action="VDL"))

    builder.adjust(1)
    return builder.as_markup()