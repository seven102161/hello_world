import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from lxml import etree


class CmbProduct(object):

    def __init__(self, url, page):
        self.url = url
        self.browser = webdriver.Chrome()
        self.contents = ''
        self.main()
        self.page = page

    def main(self):
        while True:
            self.browser.get(self.url)
            self.get_html()
            if self.page == 0:
                break
            # self.browser.close()

    def get_html(self):
        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="bottomPager"]/div/a[5]')))
        self.contents = self.browser.page_source
        self.parse_contents()
        self.page -= 1
        time.sleep(3)
        self.next_page()

    def next_page(self):
        self.browser.find_element_by_xpath('//*[@id="bottomPager"]/div/a[5]').click()
        self.get_html()

    def parse_contents(self):
        tree = etree.HTML(self.contents)
        div_list = tree.xpath('//div[@class="c_list"]/div[@class="prdBlock"]')
        try:
            for div in div_list:
                product_id = div.xpath('.//div[@class="cdleftArea"]/div/div[2]/text()')[0]
                print(product_id)
        except Exception as e:
            print(e)
            pass


cmb_url = r'https://www.cmbchina.com/cfweb/CDeposit/Default.aspx'
cmb_china = CmbProduct(cmb_url, 1)

