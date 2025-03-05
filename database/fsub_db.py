import motor.motor_asyncio
from typing import Optional
from info import AUTH_CHANNEL, DATABASE_URI

class Fsub_DB:
    """
    This is a class to handle all database operations for all the incoming join requests on the Fsub Channel.
    This class includes the following functions to handle the user data:\n
        • add_user() :- This function accepts the user ID, first name, username and the date as parameters and save it in the DB.\n
        • get_user() :- This function accepts the user ID as arguement and searches with it on DB and returns the user details.\n
        • get_all_users() :- This function doesn't have any arguements and it returns all the users' details from DB.\n
        • delete_user() :- This function accepts the user ID as arguements and it deletes the user details from DB which have the given user ID.\n
        • purge_users() :- This function doesn't have any arguements and it doesn't return anything. It just deletes all the users' details from DB.\n
        • total_users() :- This function doesn't have any arguements and it returns the total number of users in DB (int value).

    For any paid edits, contact @creatorbeatz on Telegram !
    """

    def __init__(self) -> None:
        self.client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
        self.db = self.client["Fsub_DB"]
        self.col = self.db[str(AUTH_CHANNEL)]

    async def add_user(self, id: int, f_name: str, username: str, date: str) -> None:
        await self.col.insert_one(
            {
                'id': int(id),
                'first_name': f_name,
                'username': username,
                'date': date
            }
        )

    async def get_user(self, id: int) -> Optional[dict]:
        return await self.col.find_one(
            {
                'id': int(id)
            }
        )
    
    async def get_all_users(self) -> Optional[list]:
        return await self.col.find().to_list(None)
    
    async def delete_user(self, id: int) -> None:
        await self.col.delete_one(
            {
                'id': int(id)
            }
        )

    async def purge_users(self) -> None:
        await self.col.delete_many({})

    async def total_users(self) -> int:
        return await self.col.count_documents({})
