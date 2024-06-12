# -*- coding: utf-8 -*-
'''
脚本用于巨量的自动添加公网ip白名单
添加变量名=JuLiang_Whitelist   变量值=备注#trade_no业务号#api密钥
多账户换行
需要安装依赖asyncio、requests
cron: */30 * * * *
new Env('巨量白名单');
'''


import requests
import os
import asyncio
import hashlib

async def get_public_ip():
    print('开始获取当前公网')
    response = requests.get('http://ip-api.com/json')
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            return data['query']
    return None

async def env_init(ip):     # 获取环境变量
    juliang_envs = os.environ.get("JuLiang_Whitelist")
    if juliang_envs:
        trade_no_keys = juliang_envs.splitlines()
        for trade_no_key in trade_no_keys:
            username, trade_no, key = trade_no_key.split("#")
            await add_ip(username, ip, trade_no, key)  # 添加白名单
    else:
        print("没有找到JuLiang_Whitelist变量")


async def calculate_md5(input_string):
    md5_hash = hashlib.md5()    # 创建一个 md5 哈希对象
    md5_hash.update(input_string.encode('utf-8'))    # 更新哈希对象与输入字符串编码为字节
    return md5_hash.hexdigest()    # 计算哈希值并以十六进制格式返回


async def add_ip(username, ip, trade_no, key):  # 添加ip
    sign = await calculate_md5(f"new_ip={ip}&reset=1&trade_no={trade_no}&key={key}")
    response = requests.get(f"http://v2.api.juliangip.com/dynamic/replaceWhiteIp?new_ip={ip}&reset=1&trade_no={trade_no}&sign={sign}")
    if response.status_code == 200:
        print(f"{username} 提交白名单成功")
    else:
        print(f"{username} 提交白名单失败，手动请求试试……")



async def main():
    ip = await get_public_ip()
    if ip:
        print("当前公网IP地址是:", ip)
    else:
        print("无法获取当前公网IP地址")
    await env_init(ip)


asyncio.run(main())
