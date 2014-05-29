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
hosturl = 'http://xk.urp.seu.edu.cn/' #自己填写  
#post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）  
posturl = 'http://xk.urp.seu.edu.cn/jw_css/system/login.action' #从数据包中分析出，处理post请求的url  
  
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


#urllib.request.urlretieve('http://xk.urp.seu.edu.cn/jw_css/getCheckCode','E:\\lovecode\\1.jpg')
#构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。  
headers = { 'Host' : 'xk.urp.seu.edu.cn',
            'Proxy-Connection' : 'keep-alive',
            'Origin' : 'http://xk.urp.seu.edu.cn',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Referer' : 'http://xk.urp.seu.edu.cn/jw_css/system/login.action'
            
           }  
#构造Post数据，他也是从抓大的包里分析得出的。  
postData = {
            'userId' : '213111455', #你的用户名  
            'userPassword' : 'ft4969464', #你的密码，密码可能是明文传输也可能是密文，如果是密文需要调用相应的加密算法加密  
            'checkCode' : code,   #特有数据，不同网站可能不同  
            'x' : '33',  #特有数据，不同网站可能不同
            'y' : '5'
  
            }  
  
#需要给Post数据编码  
postData = urllib.urlencode(postData)  
  
#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  

request = urllib2.Request(posturl, postData, headers)
print request
response = urllib2.urlopen(request)  
text = response.read().decode('utf-8')  
print text  
