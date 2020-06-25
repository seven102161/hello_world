import requests
from urllib import parse
from bs4 import BeautifulSoup
import time
import random
import json
from get_proxy import get_proxy


def write_to_json(info):
    with open('an_business.json', 'w', encoding='utf-8') as fp:
        json.dump(info, fp)
    print('写入成功！')


def get_info(content):
    item = dict()
    soup = BeautifulSoup(content, features='html.parser')

    try:
        building = soup.select('#basic-info > div:nth-child(15) > span.value')[0].text
        item['building'] = building

        floor = soup.select('#basic-info > div:nth-child(10) > span.value')[0].text
        item['floor'] = floor

        address = soup.select('#basic-info > div:nth-child(17) > span.value')[0].text
        item['address'] = address

        size = soup.select('#basic-info > div:nth-child(6) > span.value')[0].text
        item['size'] = size

        daily_price = soup.select('#basic-info > div:nth-child(3) > span.value')[0].text
        item['daily_price'] = daily_price

        monthly_price = soup.select('#basic-info > div:nth-child(5) > span.value')[0].text
        item['monthly_price'] = monthly_price

    except Exception:
        print('nothing was founded')

    print(item)
    return item


def get_contents(full_list, *url_list):
    global proxy_list
    global an_house_info
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.13 Safari/537.36',
        'referer': full_list,
    }
    proxies = random.choice(proxy_list)
    for url in url_list:
        response = requests.get(url, headers=headers, proxies={'http': proxies})
        an_house_info.append(get_info(response.text))
        time.sleep(random.randint(1, 5))


def get_url(html):
    soup = BeautifulSoup(html, features='html.parser')
    layout = soup.find('div', {'class': "layout"})
    content = layout.find('div', {'class': "list-content"})
    items = content.find_all('div', {'class': "list-item"})

    url_list = []
    for i in items:
        url = i('a')[1].get('href')
        url_list.append(url)

    return url_list


def get_html(pg, loc):
    global proxy_list
    base_url = 'https://qd.sydc.anjuke.com/xzl-zu/p'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.13 Safari/537.36',
    }

    for i in range(pg):
        pg = str(i + 1)
        params = {
            'kw': loc,
        }
        extend_url = parse.urlencode(params)
        full_url = base_url + pg + '/?' + extend_url
        proxies = random.choice(proxy_list)
        response = requests.get(full_url, headers=headers, proxies={'http': proxies})
        if response.status_code == 200:
            url_list = get_url(response.text)
            print('page', i, 'url list get')
            get_contents(full_url, *url_list)
        else:
            print('page', i, 'failed')
        time.sleep(5)


def main():
    page = 1
    loc = '国际创新园'
    get_html(page, loc)
    write_to_json(an_house_info)


if __name__ == '__main__':
    proxy_list = get_proxy()
    an_house_info = []
    main()
