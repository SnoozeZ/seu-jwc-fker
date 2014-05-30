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
import time


#####参数#####
userName = '213111455'  #一卡通号
passWord = 'ft4969464'  #一卡通号
semester = 2            #学期编号，短学期为1，长学期为2
sleepTime = 0.5          #每尝试选课一次，延迟的时间，单位秒（0为不休眠，小心被T）
#####参数#####


def postXuan(course):
    hosturl ='http://xk.urp.seu.edu.cn'
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh='+course[1]+'&select_xkkclx='+course[2]+'&select_jhkcdm='+course[0]
    headers = { 'Host' : 'xk.urp.seu.edu.cn',
            'Proxy-Connection' : 'keep-alive',
            'Content-Length' : '2',
            'Accept' : 'application/json, text/javascript, */*',
            'Origin':'http://xk.urp.seu.edu.cn',
           'X-Requested-With': 'XMLHttpRequest',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
          }
    postData = {'{}':''
        }
    postData = urllib.urlencode(postData)
    request = urllib2.Request(posturl, postData, headers)
    response = urllib2.urlopen(request)  
    text = response.read().decode('utf-8')  
 #   print text
    return text

def stateCheck(text):
    
    if (text.find(u'成功选择') != -1)or(text.find(u'服从推荐') != -1):
        return 0
    if text.find(u'已满') != -1:
        return 1
    if text.find(u'失败') != -1:
        return 2
    
    
  
#登录的主页面  
hosturl = 'http://xk.urp.seu.edu.cn/' 
#post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）  
posturl = 'http://xk.urp.seu.edu.cn/jw_css/system/login.action' 
  
#设置一个cookie处理器
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
urllib2.install_opener(opener)  
  
 
h = urllib2.urlopen(hosturl)                                            #打开登录主页面，装载cookie 
image = urllib2.urlopen('http://xk.urp.seu.edu.cn/jw_css/getCheckCode')
f = open('code.jpg', 'wb')
f.write(image.read())
f.close()

code = raw_input('我眼睛不好，帮我看个东西吧。请打开我所在目录下的code.jpg，并在这里敲入里面的四位数字\n')

#登录的包：
#构造header
headers = { 'Host' : 'xk.urp.seu.edu.cn',   
            'Proxy-Connection' : 'keep-alive',
            'Origin' : 'http://xk.urp.seu.edu.cn',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Referer' : 'http://xk.urp.seu.edu.cn/jw_css/system/login.action'
            
           }  
#构造Post数据 
postData = {
            'userId' : userName,       #你的用户名  
            'userPassword' : passWord, #你的密码，  
            'checkCode' : code,           #验证码 
            'x' : '33',     #别管
            'y' : '5'       #别管2
  
            }

print('我在帮你登陆..')
postData = urllib.urlencode(postData)  #Post数据编码   
request = urllib2.Request(posturl, postData, headers)#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程 
response = urllib2.urlopen(request)  
text = response.read().decode('utf-8')  
#print text


####################################################################
#构造择学期的包：
####################################################################
print('登录成功，我去打六秒的盹..免得jwc说我操作过快')
time.sleep(6)      #防止出现'操作过快'提示
xq = str(semester)           #学期
geturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runXnXqmainSelectClassAction.action?Wv3opdZQ89ghgdSSg9FsgG49koguSd2fRVsfweSUj=Q89ghgdSSg9FsgG49koguSd2fRVs&selectXn=2014&selectXq='+xq+'&selectTime=2014-05-30%2013:30~2014-06-07%2023:59'
hosturl = 'xk.urp.seu.edu.cn'
headers = { 'Host' : 'xk.urp.seu.edu.cn',
            'Proxy-Connection' : 'keep-alive',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',        
           }
getData = {}
print('我在给你选择学期..')
getData = urllib.urlencode(getData)
request = urllib2.Request(geturl, getData, headers)
response = urllib2.urlopen(request)
text = response.read().decode('utf-8')  
#print text

#########################
#匹配可以“服从推荐”，并且没有选上的课程
#########################
print('我开始给你自动刷课了!')
courseLish = []
pattern = re.compile(r'\" onclick=\"selectThis\(\'.*\'')
#pattern = re.compile(r'selectThis')
pos=0
m=pattern.search(text,pos)
while m:
    pos=m.end()
    tempText = m.group()
    id1 = tempText[23:31]       #第一个编号
    id2 = tempText[34:51]       #第二个编号
    id3 = tempText[54:56]       #第三个编号
    course = [id1,id2,id3,1]
    courseLish.append(course)
    m=pattern.search(text,pos)  #寻找下一个

times = 0
success = 0
while True:
    times = times+1
    print "\n第"+str(times)+"次选课，已经成功选择"+str(success)+"门"

    for course in courseLish:     
        if course[3] == 1:
            back = postXuan(course)       #发送选课包
            flag = stateCheck(back)
            if 0 == flag:
                course[3] = 0
                success = success+1
                print '课程'+str(course[0])+" 选择成功"
            if 1 == flag:
                print '课程'+str(course[0])+" 名额已满"
            if 2 == flag:
                print '课程'+str(course[0])+" 选课失败，原因未知"
        time.sleep(sleepTime)


       



