import aiohttp
import asyncio

from .. models import User
from .. config import Config 


async def fetch_auth(user:User):
    url = f"{Config.API_HOST}:{Config.API_PORT}/auth"
    body = {
        "id" : user.id,
        "phone" : user.phone,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=body) as resp:
            auth = await resp.json()
            print(auth)
            return auth