#!/usr/bin/env python
# -*- coding:utf8 -*-
# Author:Dong Ye


from shopping.core.login import check_auth,check_admin
from core import tool
from conf import logger
# from conf import config
trans_logger = logger.logger('tran')   #导入日志功能模块，参数为tran，该参数是在config中提前定义好的


@check_auth  #调用装饰器，账户登录状态为True的才可以访问
def account_info(account_data):  #定义账户信息函数
    acc_message = tool.account_load(account_data['account_id'])  #重新加载一次账户id的存储信息，防止金额误差。

    user_info = '''
\033[32m客户{username}的信用卡信息: \033[0m
             \033[30m "卡号": {card_id} \033[0m
             \033[30m "信用额度": {credit} \033[0m
             \033[30m "剩余额度": {balance} \033[0m
             \033[30m "储蓄额度": {seving} \033[0m
             \033[30m "开卡时间": {enroll_date} \033[0m
             \033[30m "过期时间": {expire_date} \033[0m
             \033[30m "用户状态": {status} \033[0m
            '''.format(username=acc_message['username'],\
                                                    card_id=acc_message['account_id'],\
                                                    credit=acc_message['credit'],\
                                                    balance=acc_message['balance'],\
                                                    seving=acc_message['seving'],\
                                                    enroll_date=acc_message['enroll_date'],\
                                                    expire_date=acc_message['expire_date'],\
                                                    status=acc_message['status'],)
    return user_info  #返回格式化好的用户信息

@check_auth  #调用装饰器，账户登录状态为True的才可以访问
def repay(account_data):  #定义还款函数
    acc_data = tool.account_load(account_data['account_id']) #重新加载一次账户id的存储信息，防止金额误差。
    current_balance_1 = tool.current_balance_1(acc_data)  #打印当前账户信息
    print(current_balance_1)

    flag = True   #定义退出标记
    while flag:  #如果为True则开始循环。
        repay_amount = input("请输入还款金额，确认请按‘b’：")  #提示用户输入金额
        if len(repay_amount) > 0 and repay_amount.isdigit():  #如果输入的不为空，并且是个整数
            #调用算法函数进行还款：并将事物日志、账户信息、交易类型、交易金额传参，返回还款总额金额、利息、手续费
            new_balance,interest_balance,tip_balance = tool.tran(trans_logger,acc_data,'repay',repay_amount)
            if new_balance:  #如果还款总额有值
                #则打印当前用户交易后的还款总额
                current_balance_2 = tool.current_balance_2(repay_amount, interest_balance, tip_balance, 'repay', \
                                                           acc_data=acc_data)
                print(current_balance_2)
                #flag == False
        elif repay_amount == 'b' or repay_amount == 'B':  #按B或者b退出
            return "还款金额已保存！！"

        else:
            print("不是有效数字，请重新输入！！！")





@check_auth   #调用装饰器，账户登录状态为True的才可以访问
def withdraw(account_data): #定义提款函数
    acc_data = tool.account_load(account_data['account_id']) #重新加载一次账户id的存储信息，防止金额误差。
    current_balance_1 = tool.current_balance_1(acc_data)  #打印当前账户信息
    print(current_balance_1)

    flag = True
    while flag:
        withdraw_amount = input("请输入提取资金的额度, 确认请按‘b’：")  #提示用户输入金额
        if len(withdraw_amount) > 0 and withdraw_amount.isdigit(): #如果输入的不为空，并且是个整数
            #调用算法函数进行提款：传参事物日志、账户信息、交易类型、交易金额，并返回取款总额金额、利息、手续费
            new_balance,interest_balance,tip_balance = tool.tran(trans_logger,acc_data,'withdraw',withdraw_amount)
            if new_balance: #如果取款总额有值
                #则打印当前用户交易后的取款总额
                current_balance_2 = tool.current_balance_2(withdraw_amount, interest_balance, tip_balance, 'withdraw',\
                                                           acc_data=acc_data)
                print(current_balance_2)

        elif withdraw_amount == 'b':  #按B或者b退出
            return "还款金额已保存！！"
        else:
            print("不是有效数字，请重新输入！！！")


@check_auth  #调用装饰器，账户登录状态为True的才可以访问
def transfer(account_data):  #定义转账函数
    acc_data = tool.account_load(account_data['account_id'])  #重新加载一次账户id的存储信息，防止金额误差。
    current_balance_1 = tool.current_balance_1(acc_data)  #打印当前账户信息
    print(current_balance_1)

    flag = True
    while flag:
        inp_account_id = input("请输入需要转入的账户ID：")   #提示用户输入ID
        user_data = tool.account_load(inp_account_id)   #加载用户输入的ID账户信息
        if user_data:
            transfer_amount = input("请输入转账金额, 确认请按‘b’：")  #用户输入转账金额
            if len(transfer_amount) > 0 and transfer_amount.isdigit():  #输入的金额不为空，并且是整数
                #调用算法函数进行取款：传参事物日志、账户信息、交易类型、交易金额，并返回取款总额金额、利息、手续费
                new_balance,interest_balance,tip_balance = tool.tran(trans_logger, acc_data, 'transfer', transfer_amount)
                if new_balance:  #如果转账总额不为空
                    #打印转账后的账户信息
                    current_balance_2 = tool.current_balance_2(transfer_amount, interest_balance, tip_balance, 'transfer', acc_data=acc_data)
                    print(current_balance_2)
                     #调用算法函数进行还款：传参事物日志、账户信息、交易类型、交易金额，并返回还款总额金额、利息、手续费
                    transfer_user_balance,interest_balance,tip_balance = tool.tran(trans_logger, user_data, 'repay', transfer_amount)
                    if transfer_user_balance:   #如果还款总额不为空
                        return  "转账成功！！！"  #返回转账成功

            elif transfer_amount == 'b' or transfer_amount == 'B':
                return "还款金额已保存！！"
            else:
                print("不是有效数字，请重新输入！！！")
        else:
            print("输入的账户无效！！！")



def bills(account_data):
    acc_data = tool.account_load(account_data['account_id'])
    user_info = '''
\033[32m客户{username}的信用卡信息: \033[0m
            \033[30m "卡号": {card_id} \033[0m
            \033[30m "信用额度": {credit} \033[0m
            \033[30m "剩余额度": {balance} \033[0m
            \033[30m "储蓄额度": {seving} \033[0m
    '''.format(username=acc_data['username'],\
               card_id=acc_data['account_id'],\
               credit=acc_data['credit'],\
               balance=acc_data['balance'],\
               seving=acc_data['seving'])
    return user_info

