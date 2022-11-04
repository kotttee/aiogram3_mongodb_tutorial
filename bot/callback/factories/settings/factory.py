from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from bot.configuration import Configuration
from .translations import *


class SettingsCallbackFactory(CallbackData, prefix="main_callback"):
    action: str
    value: str

    @staticmethod
    async def settings_kd_fab(lang_code: str) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for k, v in globals()[lang_code]['settings'].items():
            builder.button(
                text=v,
                callback_data=SettingsCallbackFactory(action="get_settings", value=k)
            )
        builder.adjust(2)
        return builder.as_markup()

    @staticmethod
    async def language_kd_fab() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for lang in Configuration.available_languages():
            builder.button(
                text=lang,
                callback_data=SettingsCallbackFactory(action="change_language", value=lang)
            )
        builder.button(
            text='⛔',
            callback_data=SettingsCallbackFactory(action='get_settings', value='cancel')
        )
        return builder.as_markup()

    @staticmethod
    async def accept_kd_fab() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()

        builder.button(text='✅')
        builder.button(text='⛔')

        return builder.as_markup(resize_keyboard=True)
