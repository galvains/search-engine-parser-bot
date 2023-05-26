import time
import asyncio

import aiohttp
from aiogram import types
import json

from fake_useragent import UserAgent


# Парсинг каждого таска(страницы)
async def collect_data(session, page: int, headers: dict, obj_name: str, obj_art: int,
                       message: types.Message, start_time):
    url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&page={page}&' \
          f'query={obj_name}&regions=80,115,38,4,64,83,33,68,70,69,30,86,75,40,1,66,110,22,31,48,71,114&' \
          f'resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false'

    async with session.get(url=url, headers=headers, ssl=False) as response_session:
        data = await response_session.read()
        response = json.loads(data)

        products = list()
        data = response.get('data', {}).get('products', None)

        if data:
            for elem in data:
                products.append({
                    'article': elem.get('id', None),
                    'name': elem.get('name', None)
                })

        result = find_element(data=products, obj_art=obj_art, page=page)

        if result:
            await message.reply(f'Card: <b>"{result[2]}"</b>\nNumber: <b>{result[0]}</b>\n'
                                f'Page_number: <b>{result[1]}</b>\nTime: <b>{round((time.time() - start_time), 2)}</b>'
                                f' sec.', parse_mode='HTML')


# Поиск элемента на странице
def find_element(data: list, obj_art: int, page: int):
    for element in data:
        if element['article'] == obj_art:
            return data.index(element) + 1, page, element['name']
    else:
        return False


# Создание пула тасков (каждый таск - отдельная страница)
async def gather_data(obj_name: str, obj_art: int, message: types.Message, start_time):
    url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&' \
          f'filters=xsubject&query={obj_name}&' \
          f'regions=80,115,38,4,64,83,33,68,70,69,30,86,75,40,1,66,110,22,31,48,71,114&' \
          f'resultset=filters&spp=0'

    ua = UserAgent()
    headers = {
        'User-Agent': str(ua.random)
    }

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers, ssl=False)
        data = await response.json(content_type='text/plain')
        paginate = int(data.get('data').get('total') / 100) + 1
        # print(paginate)
        tasks = []

        for page in range(1, paginate + 2):
            task = asyncio.create_task(collect_data(session, page, headers, obj_name, obj_art, message, start_time))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    obj_name = input('enter query: ')
    obj_art = int(input('enter article: '))
    start_time = time.time()

    asyncio.run(gather_data(obj_name, obj_art))

    print(time.time() - start_time)


if __name__ == '__main__':
    main()
