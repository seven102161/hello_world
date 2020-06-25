import requests
import time
from bs4 import BeautifulSoup


def get_proxy():
    base_url = 'https://www.kuaidaili.com/free/inha/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'Referer': 'https://www.kuaidaili.com/free/inha/1/',
    }
    proxy_list = []
    for i_ in range(2):
        full_url = base_url + str(i_ + 1)
        print(f'get {i_ + 1} page')
        response = requests.get(full_url, headers=headers)
        soup_p = BeautifulSoup(response.text, features='html.parser')
        t_body = soup_p.select('#list > table > tbody')[0]
        trs = t_body.find_all('tr')
        for tr in trs:
            ip = tr.find('td', {'data-title': "IP"}).text
            port = tr.find('td', {'data-title': "PORT"}).text
            proxy = 'http://' + ip + ':' + port
            proxy_list.append(proxy)
        time.sleep(10)
    print('done')
    return proxy_list


def main():
    get_proxy()


if __name__ == '__main__':
    main()

