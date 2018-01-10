#!/usr/bin/env python
# -*- coding:utf8 -*-
# Author:Dong Ye

from conf import config
from core import login
from conf import logger
from core import tool
from core import transaction

user_data = config.USER_MSG    #初始化用户登录状态
login_log = logger.logger('login')  #初始化日志格式

def run():    #定义atm功能模块的主函数
    '''
    1、利用反射原理，调用login模块下的登录、注册、退出等功能。
    2、利用反射原理，调用登录后的各种交易事物，并return值
    '''

    login_list = config.login_register  #定义登录界面列表
    login_dict = config.login_register_dict #定义登录界面列表字典
    atm_list = config.atm_trading  #定义事务种类模块列表
    atm_dict = config.atm_trading_dict  #定义事务种类模块列表字典

    flag = True   #定义退出标签
    while flag:  #如果为真就循环
        print(login_list)  #打印登录界面列表
        login_fun = tool.menu_show(login, login_dict)  #调用模块判断函数，来判断用户选择事务种类模块是否存在

        if login_fun:  #如果选择的事务模块存在
            acc_data = login_fun(user_data, login_log)  #调用事务功能模块，并将账户信息和日志功能
            # print('用户交互的账户数据>>> %s' % acc_data)
            # print('用户的登录状态>>> ',user_data)
            while acc_data:   #如果账户认证登录成功
                print(atm_list)   #打印atm事务种类界面
                atm_fun = tool.menu_show(transaction,atm_dict)  #调用模块判断函数，来判断用户选择事务种类模块是否存在
                if atm_fun:
                    ret = atm_fun(user_data)   #调用事务功能模块，（传参待定）
                    print(ret)
                    a = "\033[35m 按任意键返回上一层\033[0m".center(60, '=' )
                    input(a)
        else:
            login_log.error("The input number does not exist!!!")  #如果用户输入的编号不存在，则打印错误日志



'''
def run():

    被调用的主接口程序，功能如下：
    1、根据login模块的功能函数，来判断用户输入的操作行为：
    2、通过反射的方式，来实现不同的功能选项，尽量避免过多的if判断
    :return:


    menu_list = config.login_register  #声明用户登录的显示列表
    menu_dict = config.login_register_dict #声明用户登录列表的数字与函数字典
    flag = True   #退出循环
    while flag:   #如果为真
        print(menu_list)  #打印列表
        #time.sleep(0.1)   #防止error的日志打印时串行，用sleep延迟一段时间在进行下一步操作
        inp = input("请选择编号>>> ").strip()    #用户根据登录列表输入对应的编号
        if inp in menu_dict:    #判断，如果用户输入的内容，在对应的登录字典中时
            login_inp = menu_dict[inp]   #从字典中选择用户输入的值
            if hasattr(login,login_inp):  #如果用户输入值在login模块中
                fun = getattr(login,login_inp)  #就获取login模块中的用户输入函数
                acc_data = fun(user_data,login_log)  #执行login的用户输入函数并赋值
                print('用户交互的账户数据>>> %s' % acc_data)
                print('用户的登录状态>>> ',user_data)
                flag = False    #run模块执行完，退出while循环
        else:
            login_log.error("The input number does not exist!!!")  #打印错误日志


'''