# -*- coding: utf-8 -*-
'''
脚本用于携趣的自动添加公网ip白名单
添加变量名=xiequ_uid_ukey    变量值=备注#uid#ukey
多账户换行
需要安装依赖asyncio、requests
cron: */30 * * * *
new Env('携趣白名单');
'''


import requests
import os
import asyncio


async def get_public_ip():
    print('开始获取当前公网')
    response = requests.get('http://ip-api.com/json')
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            return data['query']
    return None



async def env_init(ip):     # 获取环境变量
    uid_ukey_envs = os.environ.get("xiequ_uid_ukey")
    if uid_ukey_envs:
        uid_ukeys = uid_ukey_envs.splitlines()
        for uid_ukey in uid_ukeys:
            username, uid, ukey = uid_ukey.split("#")
            await del_all_ip(ip, username, uid, ukey)   # 删除所有ip
            await add_ip(ip, username, uid, ukey)   # 添加白名单
    else:
        print("没有找到xiequ_uid_ukey变量")



async def del_all_ip(ip, username, uid, ukey):  # 删除所有IP网址

    response = requests.get(f"http://op.xiequ.cn/IpWhiteList.aspx?uid={uid}&ukey={ukey}&act=del&ip=all")
    if response.status_code == 200:
        print(f"{username} 清空白名单成功")
    else:
        print(f"{username} 清空白名单失败，手动请求试试……")


async def add_ip(ip, username, uid, ukey): 

    # 拼接带有IP参数的网址
    url_with_ip = f"http://op.xiequ.cn/IpWhiteList.aspx?uid={uid}&ukey={ukey}&act=add&ip={ip}"

    # 打开带有IP参数的网址
    response_with_ip = requests.get(url_with_ip)
    if response_with_ip.status_code == 200:
        print(f"{username} 白名单添加成功")
    else:
        print(f"{username} 白名单添加失败，手动请求试试……")



async def main():
    ip = await get_public_ip()
    if ip:
        print("当前公网IP地址是:", ip)
    else:
        print("无法获取当前公网IP地址")
    await env_init(ip)
    



asyncio.run(main())
