import requests
import aiohttp
import asyncio
    
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/users/get_user/123") as res:
            s = await res.json()
    print(s)

asyncio.run(main())