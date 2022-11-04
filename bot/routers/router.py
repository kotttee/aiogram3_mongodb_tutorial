from aiogram import Router, Bot
from aiogram.filters import Command, IS_NOT_MEMBER, IS_MEMBER, ChatMemberUpdatedFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommandScopeChat
from fluentogram import TranslatorRunner

from bot.commands import MainCommands
from bot.database import User

main_router = Router()


# main
@main_router.message(Command(commands=["start"]))
async def process_start_command(message: Message, _i18n: TranslatorRunner, _user: User, bot: Bot):
    await message.answer(_i18n.main.greeting())
    await bot.set_my_commands(await MainCommands.get_default_commands(_user.language),
                              BotCommandScopeChat(chat_id=_user.user_id))
    if await _user.incomplete_settings:
        await message.answer(_i18n.main.complete_settings())


@main_router.message(Command(commands=["cancel"]))
async def cancel(message: Message, state: FSMContext, _i18n: TranslatorRunner, _user: User):
    if state:
        await state.clear()
    await message.answer(_i18n.main.menu())


@main_router.message(Command(commands=["info"]))
async def info(message: Message, state: FSMContext, _i18n: TranslatorRunner, _user: User):
    if await _user.incomplete_settings:
        await message.answer(_i18n.main.complete_settings())
        return
    await message.answer(_i18n.main.info(age=_user.age))


@main_router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def handle_block(*args, _user: User):
    _user.active = False
    await _user.commit()


@main_router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def handle_unblock(*args, _user: User):
    _user.active = True
    await _user.commit()
