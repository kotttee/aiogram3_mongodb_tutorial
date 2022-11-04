from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update
from fluentogram import TranslatorHub
from bot.configuration import Configuration
from bot.database import User, Database


# several middlewares doing the same function are made in order to mitigate changes in their work in the future

class IncludeUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:

        database: Database = data['_db']
        hub: TranslatorHub = data.get('_translator_hub')
        language: str = 'en'
        user_dict = await database.get_user(event.from_user.id)

        if user_dict is None:
            if event.from_user.language_code in Configuration.available_languages():
                language = event.from_user.language_code
            data['_user'] = User(data['_db'], event.from_user.id, language)

        else:
            if user_dict['language'] in Configuration.available_languages():
                language = user_dict['language']
            data['_user'] = User(data['_db'], event.from_user.id, language,
                                 user_dict['active'], user_dict['age'])

        data['_i18n'] = hub.get_translator_by_locale(language)
        return await handler(event, data)
