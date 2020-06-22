import requests
from urllib import parse
from bs4 import BeautifulSoup
import re
import time
import json


def get_content(html):
    global an_house_info

    contents_c = re.compile(r'<ul id="houselist-mod-new" class="houselist-mod houselist-mod-new">.*?</ul>', re.S)
    content = contents_c.search(html).group()

    li = re.findall(r'<li class="list-item" data-from="">.*?</li>', content, re.S)
    for i in li:
        item = dict()
        house_info = []

        # get house url
        house_title = re.search(r'<div class="house-title">.*?</div>', i, re.S).group()
        soup_1 = BeautifulSoup(house_title, features='html.parser')
        house_url = soup_1.a['href']
        house_info.append(house_url)

        # get house details
        details = re.search(r'<div class="details-item">.*?</div>', i, re.S).group()
        soup_2 = BeautifulSoup(details, features='html.parser')
        tags = soup_2('span')

        for tag in tags[0:2]:
            # print(tag.text)
            house_info.append(tag.text)

        # get house price
        price = re.search(r'<strong>(.*?)</strong>', i).group(1)
        house_info.append(price)

        item['url'] = house_info[0]
        item['type'] = house_info[1]
        item['size'] = house_info[2]
        item['price'] = house_info[3]

        # print(item)
        an_house_info.append(item)


def get_html(page):
    base_url = 'https://shanghai.anjuke.com/sale/p'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 \
        (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    }

    for _i in range(page):
        pg = str(_i)

        params = {
            'kw': '弘辉名苑',
        }

        url_extend = parse.urlencode(params)

        full_url = base_url + pg + '-rd1/?' + url_extend + '#filtersort'
        response = requests.get(full_url, headers=headers, )
        if response.status_code == 200:
            # print(response.text)
            get_content(response.text)
            print('page', _i, 'get')
        else:
            print('page', _i, 'failed')

        time.sleep(5)


def write_to_json(info):

    with open('an_house.json', 'w', encoding='utf-8') as fp:
        json.dump(info, fp)
    print('写入成功！')


def main():
    get_html(2)
    write_to_json(an_house_info)


if __name__ == '__main__':
    an_house_info = []
    main()
