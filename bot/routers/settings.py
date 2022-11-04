from contextlib import suppress
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, Filter
from aiogram.types import Message, CallbackQuery, BotCommandScopeChat
from fluentogram import TranslatorRunner, TranslatorHub
from bot.fsm import Settings
from bot.callback import SettingsCallbackFactory as SettingsCbFac
from bot.database import User
from bot.commands import MainCommands

settings_router = Router()


@settings_router.message(Command(commands=["settings"]))
async def process_settings_command(message: Message, _i18n: TranslatorRunner, _user: User):
    await message.answer(_i18n.main.settings(),
                         reply_markup=await SettingsCbFac.settings_kd_fab(_user.language))


@settings_router.callback_query(SettingsCbFac.filter(F.action == "get_settings"))
async def get_settings(callback: CallbackQuery, callback_data: SettingsCbFac, _i18n: TranslatorRunner,
                       _user: User, bot: Bot, state: FSMContext):
    match callback_data.value:
        case 'language':
            await callback.message.answer(_i18n.main.settings.language(),
                                          reply_markup=await SettingsCbFac.language_kd_fab())
        case 'age':
            await callback.message.answer(_i18n.main.settings.age())
            await state.set_state(Settings.age)
        case 'cancel':
            await state.clear()
            with suppress(TelegramBadRequest):
                await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.answer()


@settings_router.callback_query(SettingsCbFac.filter(F.action == "change_language"))
async def change_language(callback: CallbackQuery, callback_data: SettingsCbFac, _user: User,
                          bot: Bot, _translator_hub: TranslatorHub, ):
    _user.language = callback_data.value
    await _user.commit()

    await bot.delete_my_commands(BotCommandScopeChat(chat_id=_user.user_id))
    await bot.set_my_commands(await MainCommands.get_default_commands(_user.language),
                              BotCommandScopeChat(chat_id=_user.user_id))

    _i18n = _translator_hub.get_translator_by_locale(_user.language)
    await callback.message.answer(_i18n.main.menu())

    await callback.answer()
    with suppress(TelegramBadRequest):
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)


class AgeFilter(Filter):
    def __init__(self, min_age: int, max_age: int) -> None:
        self.min_age = min_age
        self.max_age = max_age
        pass

    async def __call__(self, message: Message) -> bool:
        if message.text.isdigit():
            return self.min_age < int(message.text) < self.max_age
        return False


@settings_router.message(Settings.age, AgeFilter(0, 99))
async def change_age(message: Message, _i18n: TranslatorRunner, state: FSMContext):
    await state.update_data({'age': message.text})
    await state.set_state(Settings.accept)
    await message.answer(_i18n.main.settings.accept(),  reply_markup=await SettingsCbFac.accept_kd_fab())


@settings_router.message(Settings.accept, F.text == '⛔')
async def reject(message: Message, _i18n: TranslatorRunner, state: FSMContext, _user: User):
    await state.set_state(Settings.age)
    await message.answer(_i18n.main.settings.age())


@settings_router.message(Settings.accept, F.text == '✅')
async def accept(message: Message, _i18n: TranslatorRunner, state: FSMContext, _user: User):
    state_data = await state.get_data()
    _user.age = state_data.get('age')
    await _user.commit()
    await state.clear()
    await message.answer(_i18n.main.menu())



