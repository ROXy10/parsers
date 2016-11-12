import requests
from bs4 import BeautifulSoup
import csv

# План:
# 1. Подсчитать количество страниц
# 2. Сформировать списко урлов на стрыницы выдачи
# 3. Собрать данные


def get_html(url):
    server_request = requests.get(url)
    return server_request.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    # print(soup.find('div', class_='pagination-pages'))
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]

    return int(total_pages)


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')

    for ad in ads:
        try:
            title = ad.find('div', class_='description').find('h3').text.strip()
        except:
            title = ''

        try:
            url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
        except:
            url = ''

        try:
            price = ad.find('div', class_='about').text.strip()
        except:
            price = ''

        try:
            metro = ad.find('div', class_='data').find_all('p')[-1].text.strip()
        except:
            metro = ''

        data = {
            'title': title,
            'url': url,
            'price': price,
            'metro': metro
        }

        write_csv(data)


def write_csv(data):
    with open('avito.csv', 'a', encoding='utf-8-sig') as f:
        writer = csv.writer(f)

        writer.writerow((
            data['title'],
            data['url'],
            data['price'],
            data['metro'],
        ))

def main():
    url = 'https://www.avito.ru/moskva/telefony?p=1&q=htc'
    # 'https://www.avito.ru/moskva/telefony?p=1&q=htc'
    base_url = 'https://www.avito.ru/moskva/telefony?'
    page_part = 'p='
    query_part = '&q=htc'

    total_pages = get_total_pages(get_html(url))

    for count in range(1, 3):
        url_gen = base_url + page_part + str(count) + query_part
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)



if __name__ == '__main__':
    main()