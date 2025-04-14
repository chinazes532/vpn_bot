import aiohttp
import asyncio
import json
from typing import Any

HEADERS = {
    "Content-Type": "application/json"
}


async def outline_request(method: str, endpoint: str, data: Any = None, OUTLINE_API_KEY: str = None):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        url = f"{OUTLINE_API_KEY}{endpoint}"
        async with session.request(method, url, headers=HEADERS, json=data) as response:
            try:
                return await response.json()
            except aiohttp.ContentTypeError:
                return await response.text()


async def create_access_key(url, cert):
    return await outline_request("POST", "/access-key", OUTLINE_API_KEY=url, OUTLINE_API_CERT=cert)


async def delete_access_key(key_id: str, url, cert):
    return await outline_request("DELETE", f"/access-key/{key_id}", OUTLINE_API_KEY=url, OUTLINE_API_CERT=cert)


async def rename_access_key(key_id: str, name: str, url, cert):
    data = {"name": name}
    return await outline_request("PUT", f"/access-key/{key_id}", data, OUTLINE_API_KEY=url, OUTLINE_API_CERT=cert)


async def get_access_key_url(key_id: str):
    return await outline_request("GET", f"/access-key/{key_id}")