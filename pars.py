import requests
from bs4 import BeautifulSoup
import json
import csv

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
URL = 'https://sushihouse.by/catalog/'
HOST = 'https://sushihouse.by'

#получаем от пользователя название товара и выбираем ссылку по ключу
def urls():
    vvod_parse_url = input('Введите категорию поиска товара (Суши, Сеты, Ланч меню, HOT и салаты): ')
    url_product = {
        'Суши': 'sushi-i-rolly/?PAGEN_2=',
        'Сеты': 'sety/?PAGEN_2=',
        'Ланч меню': 'lanch-menyu/?PAGEN_2=',
        'HOT и салаты': 'goryachie-blyuda/?PAGEN_2='
    }

    for _ in url_product:
        return url_product[vvod_parse_url]

#парсим каждую страницу 
def parser(url_parse):
    list_bk = []
    url_parse = urls()

    print(
    '''    
    Суши. Доступно страниц - 11
    Сеты. Доступно страниц - 3
    Ланч меню. Доступно страниц - 2
    HOT и салаты - 4
    '''
    )

    cout_page = int(input('''Введите кол-во страниц: '''))

    for page in range(1, cout_page + 1):
        url = f'{URL}{url_parse}{page}'
        req = requests.get(url=url, headers=HEADERS)
        soup = BeautifulSoup(req.text, 'lxml')

        block_content = soup.find_all('div', class_='col-lg-3 col-xl-3 col-sm-6 product-ajax-cont')

        print(f'Парсинг страницы номер {page}')
        parse_block(block_content, list_bk)
    save(list_bk)

#собираем данные с конкретного блока
def parse_block(block_content, list_bk):
    for item in block_content:
        try:
            title = item.find('div', class_='product-info base-view').find_next().get_text()
        except AttributeError:
            continue
        popular = item.find('div', class_='product-labels')
        if popular:
            popular = ', '.join([div['title'] for div in item.find_all('div', title=True)])
        else:
            popular = 'Обычный продукт'
        price = item.find('span', itemprop='price').get_text() + ' руб.'
        recipe = item.find('div', class_='product-description base-view').text.strip()
        grams = item.find('span', class_='weight').text
        link = HOST + item.find('a', class_='product-title font-fix base-view').get('href')

        list_bk.append({
            'title': title,
            'popular': popular,
            'price': price,
            'recipe': recipe,
            'grams': grams,
            'link': link
        })

#собственно сохраняем(кто бы мог подумать)
#можно либо json либо csv
def save(listen):
    # with open ('data.json', 'w', encoding='utf-8') as file:
    #     json.dump(listen, file, indent=4, ensure_ascii=False)
    with open(f'file.csv', 'w', encoding='utf-8', newline='') as file: #'сз1251
        writer = csv.writer(file, delimiter=' ')
        writer.writerow([
            'Название', 
            'Этикетка продукта', 
            'Цена', 
            'Рецепт', 
            'Ссылка'
        ])
        for item in listen:
            writer.writerow([
                item['title'],
                item['popular'],
                item['price'], 
                item['recipe'], 
                item['grams'],
                item['link']
            ])


def main():
    parser(urls)


if __name__ == "__main__":
    main()
