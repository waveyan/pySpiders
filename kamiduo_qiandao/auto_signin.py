#! /home/ubuntu/insforpk/env/bin/python3

import requests
import json
import datetime


def main(UserId):
    url = 'http://www.zk2016.com/zk/w/index.php?s=api'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Agent-User': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69 MicroMessenger/6.5.4 NetType/WIFI Language/zh_CN',
    }
    data = {
        'UserId': UserId,
        '_api': 'SignIn/SignIn',
        '_interface': '173.67.15.240:29800'
    }

    r = requests.post(url, data=data, headers=headers)
    return json.loads(r.content.decode('utf-8'))


if __name__ == '__main__':
    try:
        myID = '6e7b20f6-2d2f-429f-9401-5d9514b138a5'
        laopoID = '86d78911-92a4-4746-9f72-1e4cc9bc5699'
        laopo = main(laopoID)
        my = main(myID)
        # laopo = {"Data":[{"Message":"签到成功,您已连续签到4次"}],"ErrorCode":"","ResultMsg":"","ResultCode":0}
        # my={"Data":[{"Message":"今日已签到，您已连续签到4次,明天再来吧"}],"ErrorCode":"","ResultMsg":"您今日已签到，明天再来吧","ResultCode":0}
        for _ in range(3):
            if laopo.get('Data')[0].get('Message').split(',')[0].strip() == "签到成功":
                print('lp响%s签左' % datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S'), end=' ')
                break
            elif laopo.get('ResultMsg') == "您今日已签到，明天再来吧":
                break
            else:
                laopo = main(laopoID)
        for _ in range(3):
            if my.get('Data')[0].get('Message').split(',')[0].strip() == "签到成功":
                print('我响%s签左' % datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S'))
                break
            elif my.get('ResultMsg') == "您今日已签到，明天再来吧":
                break
            else:
                my = main(myID)
    except Exception as e:
        print(datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S'), end=' ')
        print(e)
