import asyncio
from curl_cffi.requests import AsyncSession


async def get_response_from_urls_async(file_name_url_tuple_list):
    async with AsyncSession() as s:
        tasks = [s.get(url, impersonate="chrome120" ) for _, url in file_name_url_tuple_list]
        responses = await asyncio.gather(*tasks)

        return [(file_name_url_tuple_list[i][0], responses[i]) for i in range(len(responses))]

def batch_urls_response_download(file_name_url_tuple_list, extension='html'):
    batch_size = 1000

    for i in range(0, len(file_name_url_tuple_list), batch_size):
        batch_urls = file_name_url_tuple_list[i:i + batch_size]
        responses = asyncio.run(get_response_from_urls_async(batch_urls))
        for file_name, response in responses:
            print(response.charset)
            with open(f'exp/{file_name}.{extension}', 'w', encoding='windows-1250', errors='replace') as file:
                file.write(response.text)

