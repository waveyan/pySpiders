import requests
from bs4 import BeautifulSoup
import os
from hashlib import md5
from multiprocessing.pool import Pool

def get_pic_url_of_page(url):
    try:
        r=requests.get(url,timeout=10)
        if r.status_code==200:
            text=r.text
            bs=BeautifulSoup(text,'lxml')
            pic_links=bs.select('.view_img_link')
            return ['http:'+link.attrs['href'] for link in pic_links]
        else:
            print('请求失败')
            return []
    except Exception as e:
        print(e)
        return []

def download_pic(pic_list):
    path=os.path.join(os.getcwd(),'get')
    for pic in pic_list:
        content=requests.get(pic).content
        save=os.path.join(path,md5(content).hexdigest()+pic[-4:])
        with open(save,'wb+')as f:
            f.write(content)
        print(pic,'downloaded')


def main(url):
    pic_list=get_pic_url_of_page(url)
    download_pic(pic_list)

if __name__=='__main__':
    url='http://jandan.net/ooxx/page-%s'
    pool=Pool()
    pool.map(main,[url%i for i in range(120,100,-1)])

