import requests
import time

from fake_useragent import UserAgent


def parser(url: str, headers: dict) -> list:
    response = requests.get(url=url, headers=headers).json()

    products = list()
    data = response.get('data', {}).get('products', None)

    for elem in data:
        products.append({
            'article': elem.get('id', None),
            'name': elem.get('name', None)
        })

    return products


def find_element(data: list, obj_art: int, page: int) -> False:
    for element in data:
        if element['article'] == obj_art:
            print(f'number: {data.index(element) + 1}\npage:{page}')
            return True


def main():
    obj_name = input('enter query: ')
    obj_art = int(input('enter article: '))
    start_time = time.time()

    url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&' \
          f'filters=xsubject&query={obj_name}&' \
          f'regions=80,115,38,4,64,83,33,68,70,69,30,86,75,40,1,66,110,22,31,48,71,114&' \
          f'resultset=filters&spp=0'

    data = requests.get(url)
    paginate = int(data.json().get('data').get('total') / 100) + 1

    for page in range(1, paginate):

        url = f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&page={page}&' \
              f'query={obj_name}&regions=80,115,38,4,64,83,33,68,70,69,30,86,75,40,1,66,110,22,31,48,71,114&' \
              f'resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false'

        ua = UserAgent()
        headers = {
            'User-Agent': str(ua.random)
        }

        data = parser(url, headers)
        if find_element(data, obj_art, page):
            print(time.time() - start_time)
            break
    else:
        print('not found')


if __name__ == '__main__':
    main()
