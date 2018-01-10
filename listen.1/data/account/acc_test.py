#!/usr/bin/env python
# -*- coding:utf8 -*-
# Author:Dong Ye


import json,os,sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_PATH)

from conf import config
database = config.USER_DATA

dir_file ="{dir}\{file}\{name}.json".format(dir=database['path'],file=database['name'],name='1234')
print(dir_file)
user_info = {'account_id': '1234',
			 'password': '0cc175b9c0f1b6a831c399e269772661',
             'username': 'dy',
			 "credit": 15000,   #信用额度
			 "balance": 15000,  #本月可用额度（剩余）
			 "seving": 0,       #储蓄额度
			 "enroll_date": "2016-01-01",
			 "expire_date": "2021-01-01",
			 "status": 0,  # 0 = 正常（normal），1 = 锁定（locked），2 = 禁用（disable）
			 "debt": []   #欠款记录
			 }

with open(dir_file,'w',encoding="utf-8") as f:
    acc_data= json.dump(user_info,f)