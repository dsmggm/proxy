# -*- coding: utf-8 -*-
'''
脚本用于巨量的自动添加公网ip白名单
使用qinglong自带推送
添加变量名=JuLiang_Whitelist   变量值=备注#trade_no业务号#api密钥
多账户换行
需要安装依赖requests
cron: */30 * * * *
new Env('巨量白名单');
'''


import requests
import os
import hashlib
import logging
import notify

logging.basicConfig(level=logging.INFO)

def get_public_ip():
    logging.info('开始获取当前公网IP')
    try:
        response = requests.get('http://ip-api.com/json')
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return data['query']
    except requests.RequestException as e:
        logging.error(f"请求公网IP时出错: {e}")
    return None

def env_init(ip):
    juliang_envs = os.environ.get("JuLiang_Whitelist")
    if juliang_envs:
        trade_no_keys = juliang_envs.splitlines()
        for trade_no_key in trade_no_keys:
            username, trade_no, key = trade_no_key.split("#")
            add_ip(username, ip, trade_no, key)
    else:
        logging.warning("没有找到JuLiang_Whitelist变量")

def calculate_md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()

def add_ip(username, ip, trade_no, key):
    sign = calculate_md5(f"new_ip={ip}&reset=1&trade_no={trade_no}&key={key}")
    try:
        response = requests.get(f"http://v2.api.juliangip.com/dynamic/replaceWhiteIp?new_ip={ip}&reset=1&trade_no={trade_no}&sign={sign}")
        if response.status_code == 200:
            logging.info(f"{username} 提交白名单成功")
        else:
            logging.warning(f"{username} 提交白名单失败，手动请求试试……")
    except requests.RequestException as e:
        logging.error(f"请求添加白名单时出错: {e}")

def main():
    ip = get_public_ip()
    if ip:
        logging.info(f"当前公网IP地址是: {ip}")
        res1 = f"添加成功，当前公网IP地址是: {ip}\n"
    else:
        logging.warning("无法获取当前公网IP地址")
        res1 = "无法获取当前公网IP地址\n"

    env_init(ip)

    conversationTitle = "巨量IP更新白名单"
    content = f"{res1}"
    notify.send(conversationTitle, content)

if __name__ == "__main__":
    main()
