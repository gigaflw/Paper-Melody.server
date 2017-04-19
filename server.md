# Server

本文档将阐述如何在你自己的电脑上搭建简单的 Python 服务器

## 准备工作

1. 首先保证你有一台电脑 
2. 安装 Python, 版本任意
3. 考虑到真实工程中将使用 Flask，我还是推荐 Python 3


## Fire!

本节将建立最简单的服务器

    $ mkdir awesomesite
    $ cd awesomesite

创建你的网站文件夹

    $ echo "Jello World!" >> index.html

创建 `index.html` 文件

    $ python -m SimpleHTTPServer 8080     # py2
    $ python3 -m http.server 8080         # py3

在 8080 端口启动你的服务器

    此时此刻已经有一个服务器运行在你的电脑上了，它默认以`index.html`作为入口

    在浏览器中访问`localhost:8080`就可以看到 index.html 的内容

你应当注意到只要在同一个局域网内，任何电脑／手机都可以访问你刚才运行起来的服务器

只不过他们不能访问`localhost` ，而应当访问你的**内网 IP**

> 查看 内网IP 的方法

#### Mac

    系统偏好设置 > 网络 > “其 IP 地址为 XXXXXX”

#### Windows
    
    网络和共享中心 > 点你连上的那个网络 > 详细信息 > IPv4 地址

#### Linux

    购买一台 Mac > GOTO 1

你可以尝试在自己或室友的浏览器访问 <你刚才看到的 IP>:8080，效果和 `localhost:8080` 应该是一样的

## Flask

我们的 Python 服务器只能展示静态页面，如果要写后端代码，就有点麻烦了

此时此刻，我们需要**Flask**

> 如何搭建一个超棒的后端

1. 创建一个文件夹
2. 去看 [Flask 教程](http://flask.pocoo.org/docs/0.12/quickstart/)
3. 码
4. 完了