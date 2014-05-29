# -*- coding: cp936 -*-
#!/usr/bin/python  
#import urllib.request
import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re  
  
#登录的主页面  
hosturl = 'http://xk.urp.seu.edu.cn/' 
#post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）  
posturl = 'http://xk.urp.seu.edu.cn/jw_css/system/login.action' 
  
#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie  
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
urllib2.install_opener(opener)  
  
#打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）  
h = urllib2.urlopen(hosturl)
image = urllib2.urlopen('http://xk.urp.seu.edu.cn/jw_css/getCheckCode')
f = open('code.jpg', 'wb')
f.write(image.read())
f.close()

code = raw_input('打开code.jpg 输入里面的字符')


#构造header
headers = { 'Host' : 'xk.urp.seu.edu.cn',
            'Proxy-Connection' : 'keep-alive',
            'Origin' : 'http://xk.urp.seu.edu.cn',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Referer' : 'http://xk.urp.seu.edu.cn/jw_css/system/login.action'
            
           }  
#构造Post数据 
postData = {
            'userId' : '213111455', #你的用户名  
            'userPassword' : 'ft4969464', #你的密码，  
            'checkCode' : code,   #验证码 
            'x' : '33',  #别管
            'y' : '5'       #别管2
  
            }  
  
#需要给Post数据编码  
postData = urllib.urlencode(postData)  
  
#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  

request = urllib2.Request(posturl, postData, headers)
print request
response = urllib2.urlopen(request)  
text = response.read().decode('utf-8')  
print text  
