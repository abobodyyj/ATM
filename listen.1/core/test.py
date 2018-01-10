#!/usr/bin/env python
# -*- coding:utf8 -*-
# Author:Dong Ye



import time,datetime
import  os,sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from conf import config


#ATM用户交易事物：
def tran(tran_log,acc_data,tran_type,tran_amount,*args):
    tran_tag = config.TRANSACTION_TYPE
    tran_amount = float(tran_amount)  #用户输入额度（还、取）

    if tran_type in tran_tag:
        interest_balance = tran_amount * tran_tag[tran_type]['interest']  #利息
        tip_balance = tran_tag[tran_type]['tip']   #手续费
        old_balance = acc_data['balance']    #可用余额
        credit = acc_data['credit']          #上线总额
        seving = acc_data['seving']          #储蓄余额

        if tran_tag['action'] == 'plus':
            plus_balace = old_balance + (tran_amount - interest_balance - tip_balance)   #新可用额度
            if plus_balace >= credit:
                exceed_credit = plus_balace - credit
                seving_avg = exceed_credit +seving
                acc_data['seving']  = seving_avg
            elif plus_balace < credit:
                acc_data['balance'] = plus_balace

        elif tran_tag['action'] == 'minus':
            minus_balace = old_balance - (tran_amount + interest_balance + tip_balance)  #新取款额度
            if minus_balace <= 0:
                print("可用余额不足")
            elif minus_balace <= seving:
                seving_avg = seving - minus_balace
                acc_data['seving']  = seving_avg
            elif minus_balace > seving:
                exceed_seving = minus_balace - seving
                acc_data['seving']  = 0
                acc_data['balance'] = exceed_seving


    else:
        print('您当前%s交易类型不存在，请重新选择！！！' % (tran_type))


tran('log','u1','repay','10000')