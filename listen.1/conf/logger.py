#!/usr/bin/env python
# -*- coding:utf8 -*-
# Author:Dong Ye

import logging,os,sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from conf import config


def logger(log_tag):
    log_level = config.LOG_LEVEL

    #定义logfile的标签和级别
    logger = logging.getLogger(log_tag)  #定义日志标签
    logger.setLevel(log_level)    #定义日志全局格式

    #定义屏幕输出
    ch = logging.StreamHandler()       #定义输出介质屏幕显示
    ch.setLevel(log_level)      #定义日志级别

    #定义文件输出路径
    logfile_path = '{dir}\logs\{file}'.format(dir=config.BASE_PATH,file=config.LOG_NAME[log_tag]) #定义logfile路径
    fh = logging.FileHandler(logfile_path)  #定义输出介质日志文件
    fh.setLevel(log_level)  #定义日志文件的级别

    #定义日志格式：
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #绑定输出介质的日志格式：
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    #绑定日志标签：
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

# log = logger('login')
# log.error("打印错误提示")