from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import re
import time

# browser=webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

# browser.get('https://www.toutiao.com/')
# wait=WebDriverWait(browser,10)
# li=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.y-wrap > div.y-box.container > div.y-left.index-channel > div > div > ul > li:nth-child(4) > a')))
# li.click()
# #切换窗口
# browser.switch_to_window(browser.window_handles[1])
# browser.implicitly_wait(5)
# browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
# bs=BeautifulSoup(browser.page_source)
# for item in bs.select('.img-item'):
#     print(item)

def get_gallery_data(url,page):
    browser=webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    browser.get(url)
    for i in range(page):
        print(i)
        browser.implicitly_wait(5)
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(5)
    bs=BeautifulSoup(browser.page_source,'lxml')
    #[{},{}]
    gallery_data=[]
    for item in bs.select('.img-item'):
        data={
            'title':item.find('p',{'class':'des'}).get_text(),
            'pic-num':item.find('span',{'class':'pic-num'}).get_text()[:-1],
            'url':re.search(re.compile('<a(.*)href="(.*?)"(.*)>'),str(item.find('a'))).group(2)
        }
        gallery_data.append(data)
    return gallery_data

if __name__=='__main__':
    url='http://www.toutiao.com/ch/gallery_photograthy/'
    page=10
    for x in get_gallery_data(url, page):
        print(x)