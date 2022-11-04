import asyncio
from aiogram import Bot, Dispatcher
from bot.configuration import Configuration
from bot.multilanguage import build_translator_hub
from bot.middlewares.middlewares import IncludeUserMiddleware
from bot.database import Database
from bot.routers.router import main_router
from bot.routers.settings import settings_router

# КОМАНДА С ИНФОРМАЦИеЙ ПРО СЕБЯ НУ И В КНИЖКЕ НАПИСАТЬ МЫ СДЕЛАЕМ БОТА КТОРЫЙ ТИПА С ФЛЮЕНТОГРАМОМ И ТД


async def main():

    bot = Bot(Configuration.bot_token(), parse_mode='html')
    dp = Dispatcher()
    database = Database()

    # ROUTERS
    dp.include_router(main_router)
    dp.include_router(settings_router)

    # MIDDLEWARES
    # message
    dp.message.middleware(IncludeUserMiddleware())
    dp.callback_query.middleware(IncludeUserMiddleware())
    dp.my_chat_member.middleware(IncludeUserMiddleware())

    translator_hub = await build_translator_hub()

    # START
    await dp.start_polling(bot, _translator_hub=translator_hub, _db=database, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
