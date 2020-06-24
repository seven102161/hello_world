import requests
from urllib import parse
from bs4 import BeautifulSoup
import time
import random
import json


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
    global an_house_info
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.13 Safari/537.36',
        'referer': full_list,
    }
    for url in url_list:
        # print(url)
        response = requests.get(url, headers=headers)
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
    base_url = 'https://qd.sydc.anjuke.com/xzl-zu/p'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.13 Safari/537.36',
    }
    p_list = get_proxy()
    print(p_list)

    for i in range(pg):
        pg = str(i + 1)

        params = {
            'kw': loc,
        }

        extend_url = parse.urlencode(params)

        full_url = base_url + pg + '/?' + extend_url
        # print(full_url)
        proxies = random.choice(p_list)

        response = requests.get(full_url, headers=headers, proxies={'http': proxies})
        if response.status_code == 200:
            # print(response.text)
            url_list = get_url(response.text)
            print('page', i, 'url list get')
            get_contents(full_url, *url_list)
            write_to_json(an_house_info)
        else:
            print('page', i, 'failed')
        time.sleep(5)


def get_proxy():
    global pro
    ip_list = []
    port_list = []

    base_url = 'https://www.kuaidaili.com/free/inha/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'Referer': 'https://www.kuaidaili.com/free/inha/1/',
    }

    for i_ in range(2):
        full_url = base_url + str(i_ + 1)
        # print(full_url)
        response = requests.get(full_url, headers=headers)
        # print(response.text)

        soup_p = BeautifulSoup(response.text, features='html.parser')

        ips = soup_p.find_all('td', {'data-title': "IP"})
        for ip in ips:
            ip_list.append(ip.text)

        ports = soup_p.find_all('td', {'data-title': "PORT"})
        for port in ports:
            port_list.append(port.text)

    proxy_list = []
    for i in range(len(ip_list)):
        pro = ip_list[i] + ':' + port_list[i]
        # print(pro)
        proxy_list.append(pro)
        # print(proxy_list)
    return proxy_list


def main():
    page = 1
    loc = '万科中心'
    get_html(page, loc)


if __name__ == '__main__':
    pro = ''
    an_house_info = []
    main()
