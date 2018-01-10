#!/usr/bin/env python
# -*- coding:utf8 -*-
# Author:Dong Ye

import time
from core import tool


#用户认证登录的装饰器：(登录认证)
def check_auth(func):   #定义个装饰器函数，func为旧代码函数体
    '''
    检测用户登录的状态，只有状态为True的情况下才能继续装饰器下面的操作。
    :param func:被封装的旧代码函数体
    :return:ret是返回旧代码函数体的返回值；inner是高阶函数对旧代码函数体的封装和扩展。
    '''
    def inner(*args,**kwargs):  #定义一个嵌套函数，用于旧代码函数体的封装或者功能扩展
        if args[0].get('is_login',None):  #如果能获取到is_login状态就继续，不能获取到也不报错
            ret = func(*args,**kwargs)  #执行旧代码函数体，传参保持不变
            return ret  #return旧代码函数体的返回值
        else:    #如果不能获取到，则打印请登录。
            print('please login')
    return inner  #返回高阶函数，inner不加括号。



#用户认证登录的装饰器（权限认证）
def check_admin(func):
    '''
    用于账户登录后，某些特殊权限的账户ID可以访问特定的功能。（例如：管理员）
    :param func: 被封装的旧代码函数体
    :return: ret是返回旧代码函数体的返回值；inner是高阶函数对旧代码函数体的封装和扩展。
    '''
    def inner(*args,**kwargs): #定义一个嵌套函数，用于旧代码函数体的封装或者功能扩展
        if args[0].get('account_id',None) == '123':  #如果能获取到is_login状态就继续，不能获取到也不报错
            ret = func(*args,**kwargs)  #执行旧代码函数体，传参保持不变
            return ret #return旧代码函数体的返回值
        else:
            print('无权限查看。。。')
    return inner  #返回高阶函数，inner不加括号。




#用户登录函数：
def acc_login(user_data,login_log):
    '''
    用户登录功能，主要有：
    1、调用用户输入函数
    2、调用auth函数验证账号和密码
    3、验证成功：将用户data信息返回给run()，
    4、并记录用户id，用户名字，用户登录状态，以及账户基本信息
    5、打印日志：登录成功
    6、验证失败：打印错误信息，并重新输入。
    7、输入错误超过3次，则退出登录。
    注意：登录模块在用户认证通过够，只记录账户名，角色，登录状态，账户数据。
    :param user_data: 内存的账户状态
    :param login_log:日志功能参数
    :return: 返回账户数据信息
    '''

    retry_count = 0  #初始化计数器
    while user_data['is_login'] is not True and retry_count < 3:   #账户登录状态为False，并且重复次数小于3时开始循环。
        retry_count += 1 #循环开始，计数器+1
        #time.sleep(1) #延迟1秒
        acc_inp, pwd_result = tool.acc_pwd()  #用户输入模块
        acc_data = acc_auth(acc_inp, pwd_result)  #用户账户与加密后的md5值进行校验

        if acc_data:   #如果用户账户返回值为True
            user_data['account_id'] = acc_inp  #将用户输入的账户id保存到内存中
            user_data['is_login'] = True  #将账户登录状态设置为True
            user_data['user_data'] = acc_data  #将账户信息保存到内存中
            login_log.info('account [%s] login success' % (user_data['account_id']))
            return acc_data  #返回登录账户信息
        else:
            login_log.error("User and passwords do not exist")  #如用户账户返回值为False，则打印错误日志（账户和密码不存在）！
    else:
        login_log.error("User and passwords too many login attempts\n")   #如果账户登录状态为False，则打印错误日志（账户登录过多）


#验证模块：
def acc_auth(acc_inp,pwd_result):
    '''
    验证模块的功能如下：
    1、调用存储引擎接口模块（判断存储类型，以统一的语法获取账户id信息，定义高阶函数执行统一语法）
    2、判断账户信息返回是否为True，如果不为True则return False
    3、

    :param acc_inp: 用户输入的账户
    :param pwd_result: 用户输入的密码
    :return:
    '''
    acc_data = tool.account_load(acc_inp)  #调用存储引擎接口模块

    if acc_data:    #如果验证用户返回值为True
        account_id = acc_data['account_id']  #定义用户ID的变量
        password = acc_data['password']   #定义用户md5密码的变量
        if acc_inp == account_id:   #如果用户输入的账户id等于账户数据的id
            if pwd_result == password:  #判断用户输入的md5密码是否等于账户数据存储的md5加密密码
                acc_time = time.mktime(time.strptime(acc_data['expire_date'],"%Y-%m-%d")) #提取账户信息中的过期时间
                if acc_time > time.time():  #判断如果当前时间小于账户过期时间（有效账户）
                    return acc_data  #返回账户信息
                else:   #否则账户为过期账户
                    print('The user has expired ！！')   #打印账户已经过期
            else:  #如果密码不正确
                return False  #返回值为False

        return True   #如果用户名正确则返回True
    else:
        return False  #如果账户数据不存在则返回false


#用户注册函数：
def acc_register(user_data,login_log):
    '''
    判断用户输入的账户和密码，并返回返回值：
    如果返回值为False或者Neno，调用tool.acc_reg（账户注册的模块），进行注册。否则提示用户已经存在
    :param user_data:
    :param login_log:
    :return:
    '''
    acc_inp, pwd_result = tool.acc_pwd()  #调用用户输入模块，返回用户名密码。
    acc_data = acc_auth(acc_inp, pwd_result) #用户验证模块。

    if not acc_data:  #如果验证返回值为False
        acc_dict = tool.acc_reg(acc_inp, pwd_result)  #调用用户注册信息
        tool.account_dump(acc_dict)  #将用户信息存入到指定磁盘目录
        return False
    else:   #如果是True
        print('Accounts already exist!!! ')  #打印账户存才


#退出程序：
def quit(user_data,login_log):
    exit("退出ATM交易系统！！！")