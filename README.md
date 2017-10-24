# my_wifi_auth_server

## 搭建Django 

#### 系统版本：ubuntu 14.04 python版本：3.5.4.

#### 安装Django: sudo pip3 install Django， 安装Bloom_filter: sudo pip3 install bloom_filter-1.3-py3-none-any.whl(这个文件在Auth_server文件夹里)

#### 进入Auth_server文件夹，开启服务器：python3 manage.py runserver 0.0.0.0:8000 (8000是服务器监听端口) // 服务器是django自带的，也可以自行配置其他服务器，不过用来测试足够了，有可能提示有些第三方库找不到，根据提示可以自行安装，比较重要的有scipy和opencv。能够开启成功说明服务器配置完成。

## OpenWRT+wifidog. 路由器需要刷成OpenWRT系统，装上wifidog，需要配置：

#### 1）监听端口 2)服务器地址 3）5个脚本的地址(login, portal, msg, ping, auth)

#### 配置方法：远程登陆openwrt: ssh root@192.168.1.1， 然后修改/etc/wifidog.conf文件。

## 运行

#### 进入路由器，打开wifidog，开启服务器，手机连接wifi，使用vifi2应用拍照即可接入wifi。

## 核心代码

#### 频率提取的文件：Auth_server/Auth_app/extract.py, 其中利用工具Auth_app/dcraw将拍照所得DNG格式照片转为opencv能处理的TIFF文件。dcraw使用开源代码编译，如在不同平台上dcraw不能运行，可以自己再编译，参考网址http://www.cybercom.net/~dcoffin/dcraw/

#### 认证服务器认证逻辑实现：Auth_app/views.py。里面的不同的函数对应不同的访问地址，映射关系在Auth_server/urls.py文件里。




