import re
import json
import requests
import os
from hashlib import md5
'''今日头条图片摄影集抓取失败，无解cp，as参数'''
def get_gallery_url(url, start):
    next_max_behot_time=0
    url_list=[]
    for i in range(start):
        _as,cp=get_as_and_cp()
        print(url%(next_max_behot_time,_as,cp))
        string = requests.get(url%(next_max_behot_time,_as,cp)).text
        gallery_dict = json.loads(string)
        for j in range(11):
            url_list.append([gallery_dict['data'][j]['title'],gallery_dict['data'][j]['source_url']])
       # next_max_behot_time=gallery_dict['next']['max_behot_time']
        next_max_behot_time=int(datetime.now().timestamp())
    return url_list

def get_pic_url(url_list):
    pattern=re.compile('var gallery = (.*?);')
    pic_dict={}
    for item in url_list:
        string=requests.get('http://www.toutiao.com'+item[1]).text
        result=re.search(pattern, string)
        result=json.loads(result.group(1))
        count=int(result['count'])
        pic_dict.setdefault(item[0][10:],[])
        for i in range(count):
            pic_dict[item[0][10:]].append(result['sub_images'][i]['url'])
    return pic_dict


def download_pic(pic_dict):
    try:
        for key,value in pic_dict.items():
            path=os.path.join(os.getcwd(),'sss',key)
            if not os.path.exists(path):
                os.mkdir(path)
            print('正在下载%s'%key)
            for item in value:
                print(item)
                content=requests.get(item).content
                save_url=os.path.join(path,'%s.jpg'%md5(content).hexdigest())
                with open(save_url,'wb+') as f:
                    f.write(content)
        return True
    except Exception as e:
        print('error',e)
        return False

import math
from datetime import datetime
def get_as_and_cp():
    i=math.floor(datetime.now().timestamp())
    t=hex(i)[2:].upper()
    s=md5(str(i).encode('utf-8')).hexdigest().upper()
    if len(t)!=8:
        return ('7E0AC8874BB0985','479BB4B7254C150')
    e=s[:5]
    a=s[-5:]
    o=''.join([e[n]+t[n] for n in range(5)])
    c=''.join([t[r+3]+a[r] for r in range(5)])
    return ("A1"+o+t[-3:],t[:3]+c+'E1')



#url = "http://www.toutiao.com/api/pc/feed/?category=gallery_photograthy&utm_source=toutiao&max_behot_time=%s"
url='http://www.toutiao.com/api/pc/feed/?category=gallery_photograthy&utm_source=toutiao&max_behot_time=%s&as=%s&cp=%s'
url_list=get_gallery_url(url, 2)
print(len(url_list))
for i in url_list:
    print(i)
pic_dict=get_pic_url(url_list)
print(len(pic_dict))
#for key in pic_dict:
#    print(key)
#download_pic(pic_dict)
#print(get_cp_and_as())
