import aiohttp
import asyncio
from .. config import Config 

class API_Worker:
    def __init__(self,  **kwargs)->None:
        self.host = kwargs.get("host") or Config.API_HOST
        self.port = kwargs.get("port") or Config.API_PORT

    async def make_request(self, method, url, data=None):
        try:
            async with aiohttp.ClientSession() as session:
                response = None
                if method == "GET":
                    async with session.get(url) as _:
                        response = await _.json()
                elif method == "POST":
                    async with session.post(url, data=data) as _:
                        response = await _.json()
                elif method == "PUT":
                    async with session.put(url, json=data) as _:
                        # print(_.request_info)
                        response = await _.json()
                return response
        except Exception as e:
            print(f"Exception:{e}")

    async def mark_as_read_message(self, message):
        url = self._prepare_url("mark_as_read_appeal")
        data = { "text": message.get("text"), "telegram_id": message.get("telegram_id") }
        response = await self.make_request("PUT", url, data=data)
        return response
    
    # mark_as_read_appeal q={'text': 'string', 'telergam_id': '123', 'phone_number': 'string'}
    async def get_messages(self, _filter=None)->list:
        url = self._prepare_url("message")
        response = await self.make_request("GET", url)
        if response:
            if _filter:
                return list(filter(_filter, [x for x in response]))
            
            return [x for x in response]
       
    async def post_message(self, message):
        url = self._prepare_url("message")
        
        response = await self.make_request("POST", url, data=message)
        return response
     

    def _prepare_url(self, endpoint)->str:
        if self.port:
            return f"{self.host}:{self.port}/{endpoint}"
        return f"{self.host}/{endpoint}"