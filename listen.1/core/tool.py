#!/usr/bin/env python
# -*- coding:utf8 -*-
# Author:Dong Ye

import hashlib,time
from conf import config
from core import engine
from core import tool
# from decimal import Decimal
# from core import login
# from core import transaction






#反射函数
def menu_show(module_name,menu_dict):   #定义反射函数
    '''
    判断用户输入的功能函数是否存在模块里
    :param module_name:调用模块的名字
    :param menu_dict:用户选择的功能函数
    :return:模块中存在的功能函数
    '''

    inp = input("请选择编号>>> ").strip()  #用户输入选择的编号
    if inp in menu_dict:    #判断，如果用户输入的内容，在对应的登录字典中时
        login_inp = menu_dict[inp]   #在字典中定义用户选择的事务种类
        if hasattr(module_name,login_inp):  #如果用户输入事物种类在功能模块中
            fun = getattr(module_name,login_inp)  #就在该功能模块中获取用户输入事务种类
            return fun  #返回事务种类


#引擎接口----账户的信息读取：
def account_load(account_id):   #定义账户信息读取程序
    '''
   读取账户数据的存储引擎接口模块（tool.account_load），该模块主要有2个接口：
    1、接口：判断数据的存储引擎（file、db、redis等）。（目前db没学可以忽略）
    2、接口：利用高阶函数读取统一账户数据的语法。（不需要考虑后端是什么存储引擎，一律使用“select”和“update”的方式进行查看和保存）
    :param account_id:用户输入的账户id
    :return: 返回账户信息
    '''
    db_api = db_handle()    #无需知道存储引擎是什么类型，只做判断和调用统一接口语法的高阶函数
    acc_data = db_api("select * from account where account=%s" % account_id)  #无需知道存储引擎是什么类型。只提取统一接口语法的账户id数据
    return acc_data  #返回账户信息


#引擎接口----账户信息保存：
def account_dump(account_data):  #定义保存账户信息到磁盘
    '''
    保存账户数据的存储引擎接口模块（tool.account_dump）,该模块主要有2个接口：
    1、接口：判断数据的存储引擎（file，db，redis等）
    2、接口：利用高阶函数保存统一账户数据的语法.（不需要考虑后端是什么存储引擎，一律使用“select”和“update”的方式进行查看和保存）
    :param account_data: 用户输入的账户id
    :return: 保存成功返回True
    '''
    db_api = db_handle()  #无需知道存储引擎是什么，只做存储引擎的判断和统一接口语法的高阶函数
    acc_data = db_api("update account set username = {username} where account={account_id}". \
                      format(username=account_data['username'],account_id=account_data['account_id']), \
                      account_data_status=account_data)  #无需知道存储引擎是什么类型，只保存用户注册的账户数据


#判断用户数据的存储引擎种类
def db_handle():
    '''
    用户信息的存储引擎判断功能：
    1、存储引擎的判断函数（方便多种类型的引擎一次调用）
    2、数据存储引擎的种类标签在config.USER_DATA中进行配置,如果是数据库，可以定义数据库IP，端口，用户名，密码等连接信息。
    3、定义统一语法，提取账户id的数据（无需关心存储引擎的类型，方便扩展）
    :param user_engine_msg：是config模块下的连接存储引擎的基本信息。（存储引擎的种类不同，连接的方式也不同）
    :return: 处理用于数据统一语法的高阶函数
    '''
    user_engine_msg = config.USER_DATA   #定义连接存储引擎的方式
    if user_engine_msg['engine'] == 'file_engine': #判断存储引擎的标签是什么类型
        return engine.db_file_exec(user_engine_msg)  #调用相对应的读取和保存账户信息的存储引擎处理模块函数


#md5认证加密
def md5(user_inp_pwd):
    '''
    md5加密，用于用户登录和账户登录时的密码加密。
    :param user_inp:用户输入密码
    :return:返回加密后的信息
    '''
    obj = hashlib.md5()  #调用hashlib模块，中的md5加密算法
    obj.update(bytes(user_inp_pwd,encoding='utf-8')) #按照字节的方式将用户密码进行加密
    result = obj.hexdigest() #提取md5加密后的值
    return result  #返回md5加密后的值


#当前时间与过期时间：
def times():
    '''
    计算当前时间与2年后的时间，用于计算用户注册时的创建时间与过期时间。
    账户登录时可以判断过期时间是否大于或者小于当前时间。
    :return: 返回当前时间变量和过期时间变量
    '''
    x = time.localtime(time.time())  #获取当前时间，并转成元祖模式
    current_times = '{year}-{mon}-{day}'.format(year=x.tm_year,mon=x.tm_mon,day=x.tm_mday)  #格式化当前元祖时间
    out_times = '{year}-{mon}-{day}'.format(year=x.tm_year+2,mon=x.tm_mon,day=x.tm_mday)    #格式化2年后的元祖时间
    return current_times, out_times #返回格式化后的当前时间，和2年后的时间


#用户名和密码函数：
def acc_pwd():
    '''
    用户登录时输入账号和密码
    :return:
    '''
    acc_inp = input("account >>>").strip() #账号
    pwd_inp = input('password >>>').strip() #密码
    pwd_result = tool.md5(pwd_inp) #调用md5加密函数将密码进行加密
    return acc_inp, pwd_result #返回账号，和加密有的密码


#注册配置模板
def acc_reg(acc_inp,acc_pwd):
    '''
    用户注册，返回用户输入的账号和密码
    :param acc_inp: 用户账户(经验证后不存在的账户)
    :param acc_pwd: 密码（经过md5加密后的）
    :return: 返回用户注册信息
    '''
    acc_dict = {}   #定义空字典
    current_times,out_times = times()   #执行时间计算函数
    acc_dict['account_id'] = acc_inp           #卡号
    acc_dict['password'] = acc_pwd           #密码
    acc_dict['username'] = input("username >>>").strip()    #用户名
    acc_dict['credit'] = 15000.00                      #信用总额
    acc_dict['balance'] = 15000.00                     #信用可用余额
    acc_dict['seving'] = 0.00                          #存储余额
    acc_dict['enroll_date'] = current_times           #创建日期
    acc_dict['expire_date'] = out_times          #过期日期
    acc_dict['status'] = 0                          #用户状态（0：为正常，1：锁定，2：禁用）
    acc_dict['debt'] = []                           #欠款余额
    return acc_dict                              #返回用户注册信息


#判断用户输入的是否为整数
def numif(input_number):
    '''
    判断用户输入的是否为整数
    :param input_number: 用户输入的input
    :return: 返回判断后的input
    '''
    if input_number.isdigit():   #如果输入为整数
        int_number = int(input_number)  #则转换成int形式
        return int_number  #返回转换后的值
    else:
        return input_number  #如果输入不为整数，则返回原值。


#用户当前信息：
def current_balance_1(acc_data):
    '''
    定义用户账户的详细信息，不包括交易变更记录
    显示用户名称：
    信用上限金额：
    可用余额：
    储蓄余额：
    :param acc_data: 账户信息
    :return: 返回需要打印的格式化字符串
    '''
    current_user_balance_1 = '''
    -----------------------结算信息--------------------------------
    用户\033[31m{username}\033[0m的账户信息：
                        Credit: {credit} 元
                        Balance: {balance} 元
                        seving: {seving} 元
                    '''.format(username=acc_data['username'], \
                               credit=acc_data['credit'], \
                               balance=acc_data['balance'], \
                               seving=acc_data['seving'])
    return current_user_balance_1


#def current_balance_2(amount, interest_balance, tip_balance, tran_type, **kwargs):
def current_balance_2(*args, **kwargs):
    '''
    1、定义用户账户的交易信息：
        用户名称：
        交易类型：
        交易金额：
        信用额度上限：
        可用余额：
        储蓄余额：
        利息：
        手续费
    '''
    amount = args[0]  #定义用户输入的金额
    interest_balance = args[1]  #定义利息
    tip_balance = args[2]   #定义手续费
    tran_type = args[3]    #定义交易类型
    acc_data = kwargs.get('acc_data')   #定义账户信息字典
    current_user = '''
-----------------------结算信息--------------------------------
用户\033[31m{username}\033[0m成功\033[31m{tran_type}\033[0m{inp_amount}元：
                            Credit: {credit}
                            Balance: {balance}
                            seving: {seving}
                            interest: {interest}
                            tip: {tip}
                '''.format(username=acc_data['username'], \
                           tran_type=tran_type, \
                           inp_amount=amount, \
                           credit=acc_data['credit'], \
                           balance=acc_data['balance'], \
                           seving=acc_data['seving'], \
                           interest=interest_balance, \
                           tip=tip_balance)
    return current_user  #返回交易记录明细


#ATM用户交易事物：
def tran(tran_log,acc_data,tran_type,tran_amount,*args):
    '''
    定义还款、取款、转账的计算公式：
    :param tran_log: 事物日志
    :param acc_data: 账户信息
    :param tran_type: 交易类型
    :param tran_amount: 交易金额
    :param args: 扩展其他变量
    :return:
    '''
    tran_tag = config.TRANSACTION_TYPE   #定义交易类型的标签，其中包括利息，手续费等
    # tran_amount = Decimal(tran_amount).quantize('0.00')
    tran_amount = float(tran_amount)  #转换用户输入的额度（还、取）

    if tran_type in tran_tag:   #如果交易类型在定义的标签中
        interest_balance = tran_amount * tran_tag[tran_type]['interest']  #利息：输入金额*定义的利息百分比
        tip_balance = tran_tag[tran_type]['tip']   #手续费：定义手续费的金额
        old_balance = acc_data['balance']    #可用余额
        credit = acc_data['credit']          #上线总额
        seving = acc_data['seving']          #储蓄余额

        if tran_tag[tran_type]['action'] == 'plus':   #如果交易类型是加法
            plus_balace = old_balance + (tran_amount - interest_balance - tip_balance)   #用户还款额度=旧金额+（输入金额-利息-手续费）
            if plus_balace >= credit:  #用户还款额度　>= 上限余额
                full_balance = credit - old_balance + old_balance   #信用余额总额=（上限-旧余额+旧余额）
                seving_avg = plus_balace - full_balance  #超出信用余额的金额 = 用户还款额度 - 可用余额总额
                acc_data['balance'] = full_balance  #赋值信用总额 = 可用信用总额
                acc_data['seving']  = seving_avg + seving  #赋值储蓄总额 = 超出信用额度金额+原储蓄额度
            elif plus_balace < credit:  #如果用户还款额度 < 信用额度上限
                acc_data['balance'] = plus_balace  #用户还款额度赋值到文档里

        elif tran_tag[tran_type]['action'] == 'minus':   #如果事务类型是减法
            minus_seving = seving - (tran_amount + interest_balance + tip_balance)  #先以储蓄账户为标准，定义需要支出的金额
            # minus_balace = old_balance - (tran_amount + interest_balance + tip_balance)

            if minus_seving >= 0:  #如果支出的总金额大于等于0
                acc_data['seving'] = minus_seving #将支出的总金额赋值到账户信息里
            elif minus_seving <= 0 and old_balance > tran_amount:  #如果支出的总金额<=0 并且信用可用余额 > 支出的总金额
                zero_seving = tran_amount - seving #先扣除储蓄金额 = 用户输入的支出金额 - 储蓄金额
                consumption_balance = old_balance - zero_seving - interest_balance - tip_balance #剩余可用余额=可用余额-先扣除储蓄金额-利息-手续费
                acc_data['seving']  = 0  #将储蓄金额清零
                acc_data['balance'] =consumption_balance #将剩余可用余额赋值到账户信息用

        account_dump(acc_data)  #写入文件
        tran_log.info("account:%s   action:%s   amount:%s   interest:%s" % \
                      (acc_data['account_id'], tran_type, tran_amount, interest_balance))  #打印日志
        return acc_data,interest_balance,tip_balance  #返回账户信息，利息，手续费
    else:
        print('您当前%s交易类型不存在，请重新选择！！！' % (tran_type))