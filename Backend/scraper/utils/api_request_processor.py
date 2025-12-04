import asyncio
from typing import Any, Dict, Union

import aiohttp
import requests

from Backend.logger.log_config import log


def get_prepared_request_for_get(base_url: str, params: Dict[str, Any]) -> str:
    prepared_request = requests.Request('GET', base_url, params=params).prepare()
    return prepared_request.url


def get_json_from_url(url: str) -> Union[Dict[str, Any], str]:
    try:
        log.info(f"Executing GET: {url}")
        response = requests.get(url)
        return convert_response_to_json(response)
    except requests.exceptions.RequestException as e:
        log.error(f"Request error: {e}")
        return f"Request error: {e}"


def convert_response_to_json(response: requests.Response) -> Union[Dict[str, Any], str]:
    try:
        if response.status_code == 200:
            return response.json()
        else:
            log.warning(f"Received non-200 status code: {response.status_code}")
    except ValueError as e:
        log.error(f"JSON decoding error: {e}")
        return f"JSON decoding error: {e}"


async def get_json_from_url_async(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            json = await response.json()
            json['source_url'] = url
            return json
        else:
            log.warning(f"Received non-200 status code: {response.status}")
            return {}


async def get_json_from_urls_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(get_json_from_url_async(session, url))
        return await asyncio.gather(*tasks)


def get_json_from_urls_threaded(urls):
    return asyncio.run(get_json_from_urls_async(urls))
