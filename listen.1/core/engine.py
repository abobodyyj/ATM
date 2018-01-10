#!/usr/bin/env python
# -*- coding:utf8 -*-
# Author:Dong Ye

import os,json
from conf import config


#读取和保存账户信息的统一语法处理的高阶函数
def db_file_exec(user_engine_msg):
    '''
    定义存储引擎的连接方式功能：
    1、用于返回读取账户信息的统一语法的高阶函数。
    2、方便其他扩展。
    目的是调用高阶函数，方便多个存储引擎使用统一一个语法进行数据采集和存储，方便存储引擎的扩容。
    :param user_engine_msg:是config.USER_DATA模块下的连接存储引擎的基本信息。（存储引擎的种类不同，连接的方式也不同）
    :return: 读取和保存账户信息的统一语法的高阶函数
    '''
    file_path = '{dir}\{file}'.format(dir=user_engine_msg['path'],file=user_engine_msg['name'])  #打印文件存储的绝对路径
    return file_exec   #统一语法处理的高阶函数


#读取和保存账户信息的统一语法处理函数：
def file_exec(sql,**kwargs):
    '''
    统一语法处理功能：
    1、无论是文件存储，还是数据存储都采用统一的语法接口进行传参，这样可以很方便的扩展多个存储类型，而不影响整个代码逻辑。
    2、统一语法前端的处理方式都是固定的：
        读取数据：
            按照where进行分割
            定义文件存储的绝对路径
            判断统一语法的开头是读取数据，还是更改数据。
            在按照where右面的等号划分，并提取用户输入的账户id
            最后按照用户输入的账户id，到文件里去检索

        保存数据：
            按照where进行分割
            定义文件存储的绝对路径
            判断统一语法的开头是读取数据，还是更改数据。
            如果是更改，则找到绝对路径的目录位置
            从**kwargs万能字典形参中get获取名为account_data_status字典key
            如果有则以json的方式保存到磁盘上

    :param sql:统一语法的形参
    :param kwargs:用户注册时填写的信息模块
    :return: 读取：有记录则返回账户信息。 保存：保存成功则返回True
    '''
    acc_path = config.USER_DATA  #在重新加载一下用户存储信息，防止出现临时变更
    sql_list = sql.split('where')  #统一输入语法，与where未分割
    file_path = '{dir}\{file}'.format(dir=acc_path['path'],file=acc_path['name'])  #定义账户信息存放的绝对路径

    if sql_list[0].startswith('select') and len(sql_list) > 1:  #判断统一语法的如果是select开头
        calumn,values= sql_list[1].strip().split('=')   #将where右面的语法按照“=”再次进行拆分，并将2个值分别赋calumn values
        if calumn == 'account':  #如果calumn等于account
            file_abspath = '{dir}\{filename}.json'.format(dir=file_path,filename=values) #则按照用户输入的账户id提取json文件的绝对路径
            if os.path.isfile(file_abspath):  #判断如果json文件存在，或者该文件是个文件属性
                with open(file_abspath,'r', encoding='utf-8') as f: #只读方式打开json文件
                    user_data = json.load(f)   #将数据load出来，并赋值user_data
                    return user_data   #返回账户信息

    elif sql_list[0].startswith('update') and len(sql_list) > 1:  #如果是以update为开头 并且sql列表不为空的
        calumn,values = sql_list[1].strip().split('=')  #where 右面按照等号做分割
        if calumn == 'account':  #如果calumn等于account
            file_abspath = '{dir}\{filename}.json'.format(dir=file_path,filename=values) #提起json文件的绝对路径
            user_data = kwargs.get('account_data_status') #获取kwargs完成字典形参的值是否有名为account_data_status的kay和values

            with open(file_abspath,'w',encoding='utf-8') as f: #以写入的方式打开json文件
                json.dump(user_data,f) #将用户数据保存到磁盘中
                return True #保存成功返回True













