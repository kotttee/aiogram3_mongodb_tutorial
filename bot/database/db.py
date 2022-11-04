from bot.configuration import Configuration
from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    def __init__(self) -> None:
        client = AsyncIOMotorClient(Configuration.database_connection(), connect=True)
        database = client.aiogram3_tutorial
        self.collection = database.users

    async def get_user(self, user_id: str) -> dict | None:
        return await self.collection.find_one(dict(user_id=user_id))

    async def update_user(self, user: dict) -> None:
        old_user = await self.collection.find_one(dict(user_id=user['user_id']))
        if old_user:
            await self.collection.replace_one(dict(_id=old_user['_id']), user)
        else:
            await self.collection.insert_one(user)
