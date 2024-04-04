"""
cron: */30 * * * *
new Env('携趣自动添加白名单');
"""

#!/usr/bin/env python3

#本脚本需要requests依赖
#本脚本仅适合用于携趣白名单的自动获取

delall = 'http://op.xiequ.cn/IpW'   #填写删除所有IP的连接，参考携趣官网白名单管理接口,例如  delall = 'http://op.xiequ.cn/IpWhiteList.aspx?uid=128590&ukey=945GGGGGE068AAD02A45B7059E8E380B&act=del&ip=all'
iip = 'http://op.xiequ.cn/IpWhiteLi'    #填写添加白名单记录连接，参考携趣官网白名单管理接口,例如  iip = 'http://op.xiequ.cn/IpWhiteList.aspx?uid=128590&ukey=9G5EA120E067AAD02A45B7059E8E380B&act=add&ip='

import requests

def get_public_ip():
    url = 'https://api.ipify.org?format=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ip = data['ip']
        return ip
    else:
        return None

ip = get_public_ip()
if ip:
    print("当前公网IP地址是:", ip)
else:
    print("无法获取当前公网IP地址")

# 打开删除所有IP网址
response = requests.get(delall)

# 拼接带有IP参数的网址
url_with_ip = f"{iip}{ip}"

# 打开带有IP参数的网址
response_with_ip = requests.get(url_with_ip)
