import requests
import json
from hashlib import md5
import os

def create_param_of_url(offset,keyword):
    params={
        'offset':offset,
        'keyword':keyword,
    }
    return params

def get_pic_dict(url,params):
    data=requests.get(url,params=params)
    json_data=json.loads(data.text)
    pic_dict={}
    for items in json_data['data']:
        pic_dict.setdefault(items['title'],[])
        for pic in items['image_detail']:
            pic_dict[items['title']].append(pic['url'])
    return pic_dict

def download_pic(pic_dict):
    try:
        for title in pic_dict:
            path=os.path.join(os.getcwd(),'get',title)
            if not os.path.exists(path):
                os.mkdir(path)
            print(title)
            for url in pic_dict[title]:
                content=requests.get(url).content
                save=os.path.join(path,md5(content).hexdigest()+'.jpg')
                with open(save,'wb+') as f:
                    f.write(content)
        return True
    except Exception as e:
        print(e)
        return False

def main(i):
    url='http://www.toutiao.com/search_content/?format=json&autoload=true&count=20&cur_tab=1'
    params=create_param_of_url(i*20,'街拍')
    pic_dict=get_pic_dict(url,params)
    download_pic(pic_dict)

from multiprocessing.pool import Pool
if __name__=='__main__':
#    for i in range(5):
#        main(i)
    p=Pool()
    p.map(main,[i for i in range(5)])


