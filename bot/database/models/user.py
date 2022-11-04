from bot.database import Database


class User:

    def __init__(self, database: Database, user_id: int, language: str, active: bool | None = None,
                 age: int | None = None) -> None:
        self.database = database
        self.user_id = user_id
        self.language = language
        self.active = active
        self.age = age

    @property
    async def data(self) -> dict:
        return {
            'user_id': self.user_id, 'language': self.language, 'active': self.active,
            'age': self.age
        }

    @property
    async def incomplete_settings(self) -> bool:
        for k, v in self.__dict__.items():
            if v is None:
                return True
        return False

    async def commit(self) -> None:
        await self.database.update_user(await self.data)
