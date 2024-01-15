# 自动获取携趣代理白名单
自动获取携趣代理白名单ip，脚本需要requests依赖  
#本脚本仅适合用于携趣白名单的自动获取  

delall = '127.0.0.1'   
把127.0.0.1替换成自己的连接，用于删除所有IP的连接，参考携趣官网白名单管理接口  
例如  
delall = 'http://op.xiequ.cn/IpWhiteList.aspx?uid=128590&ukey=945GGGGGE068AAD02A45B7059E8E380B&act=del&ip=all'  

iip = '127.0.0.1'  
把127.0.01填写添加白名单记录连接，参考携趣官网白名单管理接口  
例如  
iip = 'http://op.xiequ.cn/IpWhiteList.aspx?uid=128590&ukey=9G5EA120E067AAD02A45B7059E8E380B&act=add&ip='


脚本会自动获取当前运行的公网IP并添加到白名单  
携趣的注册请自行百度
