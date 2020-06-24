import requests
from urllib import parse
from bs4 import BeautifulSoup
import re
import time
import json


def get_content(html):
    soup = BeautifulSoup(html, features='html.parser')
    layout = soup.find('div', {'class': "layout"})
    content = layout.find('div', {'class': "list-content"})
    items = content.find_all('div', {'class': "list-item"})

    for i in items:
        item = dict()

        # get url
        url = i('a')[1].get('href')
        item['url'] = url

        # get building


        # get location


def get_html(pg, loc):
    base_url = 'https://qd.sydc.anjuke.com/xzl-zu/p'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.13 Safari/537.36'
    }

    for i in range(pg):
        pg = str(i + 1)

        params = {
            'kw': loc,
        }

        extend_url = parse.urlencode(params)

        full_url = base_url + pg + '/?' + extend_url
        # print(full_url)

        response = requests.get(full_url, headers=headers, )
        if response.status_code == 200:
            # print(response.text)
            get_content(response.text)
            print('page', i, 'get')
        else:
            print('page', i, 'failed')


def main():
    page = 1
    loc = '万科中心'
    get_html(page, loc)


if __name__ == '__main__':
    an_house_info = []
    main()
