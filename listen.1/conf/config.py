#!/usr/bin/env python
# -*- coding:utf8 -*-
# Author:Dong Ye

import os,logging

#账户登录与注册：
login_register = '''
*********************************
    1、登录
    2、注册
    3、退出
*********************************
'''

login_register_dict ={
    '1': 'acc_login',
    '2': 'acc_register',
    '3': 'quit'
}



#ATM交易列表：
atm_trading = '''
*********************************
    1、账户信息
    2、还款
    3、取款
    4、转账
    5、账单
*********************************
'''


atm_trading_dict = {
    '1':'account_info',
    '2':'repay',
    '3':'withdraw',
    '4':'transfer',
    '5':'bills',
}


#用户登录状态：
USER_MSG = {
    'account_id': None,
    'is_login': False,
    'user_data':None
}

#全局日志级别：
LOG_LEVEL = logging.INFO


#日志类型：
LOG_NAME = {
    'login': 'login.log',
    'tran':'transaction.log'
}


#主目录：
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#用户存储信息：
USER_DATA = {
    'engine': 'file_engine',
    'name': 'account',
    'path': '%s\data'% BASE_PATH
}


#用户交易事物类型：
#事物名称->交易类型->利息->手续费
#注意：如果还有vip或者其他信息，可以通过装饰器，再一次修饰，然后重新定义一个vip的事务类型标签
TRANSACTION_TYPE = {
    'repay': {'action': 'plus', 'interest': 0, 'tip': 0},
    'withdraw': {'action': 'minus', 'interest': 0.05, 'tip': 0},
    'transfer': {'action': 'minus', 'interest': 0, 'tip': 10},
    }



