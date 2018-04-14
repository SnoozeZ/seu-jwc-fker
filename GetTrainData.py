# coding: utf-8

########################################################################
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                   Version 2, December 2004
#
#       Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
#   Everyone is permitted to copy and distribute verbatim or modified
#   copies of this license document, and changing it is allowed as long
#   as the name is changed.
#
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#

########################################################################


#            if you want to pack it up into EXE, Mind that you got to
#           do .encode after str


import urllib.parse
import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import re
import time
import numpy as np
import os
import cv2
from PIL import Image, ImageTk

import SEU_Decode_CNN
import URL2IMG
import tkinter as tk
cnt = 0
total = 0

WantedLessonsNameList = []
class AskAnswer(tk.Frame):
    """Foo example"""

    def __init__(self, root=None):
        """Draw Foo GUI"""
        tk.Frame.__init__(self,root)
        if(root==None):
            self.root=tk.Toplevel()

    def Ask(self,img):
        """Draw bar TopLevel window"""
        # Some uber-pythonian code here..
        self.root = tk.Toplevel()
        render = ImageTk.PhotoImage(Image.fromarray(np.uint8(img)))
        tk.Label(self.root, image=render).pack(side="top")
        e = tk.Entry(self.root)
        e.pack()
        btn = tk.Button(self.root, text='Confirm', command=self.root.destroy())
        btn.pack()
        self.root.mainloop()
        code = e.get()
        return code

aa=AskAnswer()

def getTrainData(img, code, text):
    global cnt
    if text.find('尚未开放') != -1:  # would this make it more unfair to others?
        if cv2.imwrite("E:/Python_Project/Python3.6/SEU_LES_CATCHER/TrainData/" + code + ".jpg", img) == True:


            cnt += 1
            print(str(cnt) + "训练数据已保存")
            if (cnt >= 1200):
                quit()
    else:

        global aa
        code=aa.Ask(img)
        if cv2.imwrite("E:/Python_Project/Python3.6/SEU_LES_CATCHER/TrainData/" + code + ".jpg", img) == True:


            cnt += 1
            print(str(cnt) + "训练数据已保存")
            if (cnt >= 50):
                quit()



def EvaluateModel(text):
    global total
    total += 1
    if text.find('尚未开放') != -1:
        global cnt
        cnt += 1
    if (total >= 200):
        print("验证码识别成功率 %d %%" % (int(cnt / total * 100)))
        quit()


def loginIn(userName, passWord, inputCaptcha=False):
    # 设置cookie处理器
    cj = http.cookiejar.LWPCookieJar()
    cookie_support = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    # 打开选课页面
    #	h = urllib2.urlopen('http://xk.urp.seu.edu.cn/jw_css/system/showLogin.action', timeout = 10)   # seems it is not necessary
    # 获取验证码

    for i in range(10):
        try:
            CodeImg = URL2IMG.url_to_image('http://xk.urp.seu.edu.cn/jw_css/getCheckCode')
            break
        except Exception as e:
            print(e)
            continue
    else:
        return (False, "验证码获取失败", '')

    if inputCaptcha == True:  # manually input the capthcha
        # 读取验证码
        # code = raw_input(u'请打开我所在目录下的code.jpg，并在这里敲入里面的四位数字验证码：')
        code = input('请打开我所在目录下的code.jpg，并在这里敲入里面的四位数字验证码：')  # used for exporting to exe
    else:  # automatically recognise the captcha
        code = SEU_Decode_CNN.SEU_Decode(CodeImg)

    # 构造post数据
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/system/login.action'
    header = {
        'Host': 'xk.urp.seu.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Origin': 'http://xk.urp.seu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
        'Referer': 'http://xk.urp.seu.edu.cn/jw_css/system/login.action'
    }
    data = {
        'userId': userName,
        'userPassword': passWord,  # 你的密码，
        'checkCode': code,  # 验证码
        'x': '33',  # 别管
        'y': '5'  # 别管2
    }

    # post登录数据
    (state, text) = postData(posturl, header, data)
    url = ''
    if state == True:
        if (text.find('选课批次') != -1):  # a bad label; the url returned should be the best
            print("登录成功")
            function = re.search(r'onclick="changeXnXq.*\)"', text);  # find the function whose parameter are desired
            function = function.group()
            parameters = re.search(r"'(.*)','(.*)','(.*)'\)", function)  # fetch url parameters
            url = "http://xk.urp.seu.edu.cn/jw_css/xk/runXnXqmainSelectClassAction.action?Wv3opdZQ89ghgdSSg9FsgG49koguSd2fRVsfweSUj=Q89ghgdSSg9FsgG49koguSd2fRVs&selectXn=" + parameters.group(
                1) + "&selectXq=" + parameters.group(2) + "&selectTime=" + parameters.group(3)
        else:
            state = False
            errorMessage = re.search(r'id="errorReason".*?value="(.*?)"', text)
            text = errorMessage.group(1)
            getTrainData(CodeImg,code,text)

    else:
        text = "网络错误，登录失败"
    return (state, text, url)


def selectSemester(semesterNum, url):
    print("切换学期菜单中......")
    time.sleep(5)
    # 构造选择学期的包
    # !!!NOTICE: SELECTTIME manually set this url is not a wise choice
    # geturl ='http://xk.urp.seu.edu.cn/jw_css/xk/runXnXqmainSelectClassAction.action?Wv3opdZQ89ghgdSSg9FsgG49koguSd2fRVsfweSUj=Q89ghgdSSg9FsgG49koguSd2fRVs&selectXn=2014&selectXq='+str(semesterNum)+'&selectTime=2014-05-30%2013:30~2014-06-07%2023:59'

    geturl = re.sub('selectXq=.', 'selectXq=' + str(semesterNum), url)

    header = {'Host': 'xk.urp.seu.edu.cn',
              'Proxy-Connection': 'keep-alive',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
              }
    data = {}
    # get获取学期课程
    (state, text) = getData(geturl, header, data)
    if state == True:
        if text.find("数据异常") != -1:  # switched to an unavailable semester
            state = False
            text = "目前无法选择学期" + str(semesterNum)
    return (state, text)


def postData(posturl, headers, postData):
    postData = urllib.parse.urlencode(postData).encode("utf-8")  # Post数据编码
    request = urllib.request.Request(posturl, postData, headers)  # 通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
    text = ''
    for i in range(10):
        try:
            response = urllib.request.urlopen(request, timeout=5)
            text = response.read()
            break
        except HTTPError as e:
            print("The server couldn't fulfill the request.")
            # print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            # print('Reason: ', e.reason)
        else:
            print("good!")
            # print(response.read().decode("utf8"))
            continue
    else:
        return (False, "数据发送失败")
    return (True, text.decode("utf-8"))


def getData(geturl, header, getData, returnUrl=False):
    getData = urllib.parse.urlencode(getData).encode("utf-8")
    request = urllib.request.Request(geturl, getData, header)
    text = ''
    url = ''
    for i in range(10):
        try:
            response = urllib.request.urlopen(request, timeout=5)
            text = response.read()
            url = response.geturl()
            break
        except Exception as e:
            print(e)
            print('trying to open agian...')
            continue
    else:
        if returnUrl == False:
            return (False, "获取数据失败")
        else:
            return (False, "获取数据失败", '')

    if returnUrl == False:
        return (True, text.decode("utf-8"))
    else:
        return (True, text.decode("utf-8"), url)


def stateCheck(textValue):
    text = textValue
    if (text.find('成功选择') != -1) or (text.find('服从推荐') != -1):
        return 0
    if text.find('已满') != -1:
        return 1
    if text.find('失败') != -1:
        return 2


def Mode1(semesterNum, url):
    (state, text) = selectSemester(semesterNum, url)
    if state == False:
        print(text)
        print('切换到学期' + str(semesterNum) + "失败")
        return
    else:
        print('切换到学期' + str(semesterNum) + "成功")
    # 寻找可以“服从推荐”的课程
    print("==============\n模式1，开始选课\n==============")
    courseList = []
    pattern = re.compile(r'\" onclick=\"selectThis\(\'.*\'')
    pattern2 = re.compile(r'id=\".*\" align=\"center\"\>.*\n.*\<font  class=\"style2\"\>')
    pos = 0
    m = pattern.search(text, pos)
    pos2 = 0
    m2 = pattern2.search(text, pos2)
    courseNameList = []
    while m:
        pos = m.end()
        tempText = m.group()
        m2 = pattern2.search(text, 0)
        tempText2 = m2.group()
        parameters = re.search(r"selectThis\('(.*?)','(.*?)','(.*?)'", tempText)
        parameters2 = re.search(
            r'id=\"' + parameters.group(1) + '\" align=\"center\"\>.*\n.*\<font  class=\"style2\"\>(.*?)\<', text)
        courseNameList.append(parameters2.group(1))
        course = [parameters.group(1), parameters.group(2), parameters.group(3), 1]
        courseList.append(course)
        m = pattern.search(text, pos)  # 寻找下一个

    times = 0
    success = 0
    total = len(courseList)
    for courseNames in courseNameList:
        print(courseNameList.index(courseNames) + 1, courseNames)
        # print courseNameList.index(courseNames) + 1, courseNames
    ManualChoose = True
    WantedLessons = np.zeros(total)
    if len(WantedLessonsNameList) > 0:
        ManualChoose = False
        for courseNames in courseNameList:
            for WantedLes in WantedLessonsNameList:
                if courseNames.find(WantedLes) != -1:
                    WantedLessons[courseNameList.index(courseNames)] = 1
        print("读取本地文件后，当前将要选择的课程是\n")
        for id, isWanted in enumerate(WantedLessons):
            if (isWanted):
                print(courseNameList[id])
        ManChoose = input("是否要继续选择？ [n]/y:")
        if ManChoose == 'y' or ManChoose == 'Y':  # should other cases be considered?
            ManualChoose = True

    if ManualChoose:
        while True:
            # WantedLessonsID=input(u'\n请输入需要的课程(输入0结束选择，输入-1选择全部)：')
            WantedLessonsID = eval(input('\n请输入需要的课程(输入0结束选择，输入-1选择全部)：'))
            if (WantedLessonsID == 0):
                break
            if (WantedLessonsID == -1):
                WantedLessons = np.ones(total)
                break
            WantedLessons[WantedLessonsID - 1] = 1

    while True:
        if total == 0:
            print("目前没有课可以选择")

            break
        time.sleep(0.8)  # sleeps +1
        times = times + 1
        print("\n第" + str(times) + "次选课，已成功选择" + str(success) + "门")
        for course in courseList:
            if course[3] == 1 and WantedLessons[courseList.index(course)]:
                # 构造选课post
                print("正在选择课程" + courseNameList[courseList.index(course)])
                posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh=' + \
                          course[1] + '&select_xkkclx=' + course[2] + '&select_jhkcdm=' + course[0]
                headers = {'Host': 'xk.urp.seu.edu.cn',
                           'Proxy-Connection': 'keep-alive',
                           'Content-Length': '2',
                           'Accept': 'application/json, text/javascript, */*',
                           'Origin': 'http://xk.urp.seu.edu.cn',
                           'X-Requested-With': 'XMLHttpRequest',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                           }
                data = {'{}': ''
                        }
                # post选课包，并获取返回状态
                (state, text) = postData(posturl, headers, data)
                if state == False:
                    text = '网络错误'
                else:
                    if text.find('isSuccess":"false') != -1:
                        state = False
                        text = re.search(r'errorStr":"(.*?)"', text).group(1)

                if state == True:
                    course[3] = 0
                    success += 1
                    total -= 1
                    print("Nice, 课程" + courseNameList[courseList.index(course)] + " 选择成功")
                else:
                    print("课程" + courseNameList[courseList.index(course)] + " 选课失败，" + text)


def Mode2(semesterNum, courseName, url):
    (state, text) = selectSemester(semesterNum, url)
    if state == False:
        print(text.decode('utf-8'))
        print('切换到学期' + str(semesterNum) + "失败")
        return
    else:
        print('切换到学期' + str(semesterNum) + "成功")
    print("==============\n模式2，开始选课\n==============")
    # 获取人文课页面
    geturl1 = 'http://xk.urp.seu.edu.cn/jw_css/xk/runViewsecondSelectClassAction.action?select_jhkcdm=00034&select_mkbh=rwskl&select_xkkclx=45&select_dxdbz=0'
    header1 = {
        'Host': 'xk.urp.seu.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    }
    data1 = {}
    (state, text) = getData(geturl1, header1, data1)
    if state == False:
        print("打开课程列表页面失败")
        return
    # 构造RE
    # print text

    pattern = (courseName + '.*?(\"8%\" id=\"(.{0,20})\" align)')  # possible problem here??
    # 获取课程编号
    courseNo = re.findall(pattern, text, re.S)[0][1]
    # 构造数据包
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh=' + courseNo + '&select_xkkclx=45&select_jhkcdm=00034&select_mkbh=rwskl'
    headers = {
        'Host': 'xk.urp.seu.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Content-Length': '2',
        'Accept': 'application/json, text/javascript, */*',
        'Origin': 'http://xk.urp.seu.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    }
    data = {
        '{}': ''
    }
    print("我开始选课了,课程编号：" + courseNo)
    times = 0
    while True:
        # 判断是否选到课
        times = times + 1
        (state, text) = getData(geturl1, header1, data1)
        if state == False:
            print("打开课程列表页面失败")
            return
        pattern2 = ('已选(.{0,200})align=\"')
        result = re.findall(pattern2, text, re.S)
        # print result
        success = len(result)  # 为0为不成功 继续
        if (success != 0) and (result[0].find(courseNo) != -1):
            print("Nice，已经选到课程:" + courseNo)
            break
        # 发送选课包
        print("第" + str(times) + "次尝试选择课程" + courseNo + ",但是没选到！")
        (state, text) = postData(posturl, headers, data)
        time.sleep(3)  # sleep
    return


def postRw(courseNo):
    posturl = 'http://xk.urp.seu.edu.cn/jw_css/xk/runSelectclassSelectionAction.action?select_jxbbh=' + courseNo + '&select_xkkclx=45&select_jhkcdm=00034&select_mkbh=rwskl'
    headers = {
        'Host': 'xk.urp.seu.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Content-Length': '2',
        'Accept': 'application/json, text/javascript, */*',
        'Origin': 'http://xk.urp.seu.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    }
    data = {
        '{}': ''
    }
    (state, text) = postData(posturl, headers, data)
    return (state, text)


def checkRwState(text):
    if text.find('true') != -1:  # 选课成功
        return 0
    if text.find('名额已满') != -1:
        return 1
    if text.find('冲突') != -1:
        return 2
    return -1


def Mode3(semesterNum, url):
    (state, text) = selectSemester(semesterNum, url)
    if state == False:
        print(text.decode('utf-8'))
        print('切换到学期' + str(semesterNum) + "失败")
        return
    else:
        print('切换到学期' + str(semesterNum) + "成功")
    print("==============\n模式3，开始选课\n==============")
    # 获取人文课页面
    geturl1 = 'http://xk.urp.seu.edu.cn/jw_css/xk/runViewsecondSelectClassAction.action?select_jhkcdm=00034&select_mkbh=rwskl&select_xkkclx=45&select_dxdbz=0'
    header1 = {
        'Host': 'xk.urp.seu.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    }
    data1 = {}
    (state, text) = getData(geturl1, header1, data1)
    if state == False:
        print("打开课程列表页面失败")
        return

    # 获取所有的课程编号
    pattern = ('\"8%\" id=\"(.{0,20})\" align')
    courseList = re.findall(pattern, text, re.S)
    # print courseList
    courseCtList = []
    # 找出并去掉冲突的课程
    for course in courseList:
        (state, backText) = postRw(course)
        if state == True:  # ewww bad name here
            state = checkRwState(backText)
        else:
            state = -1  # network error or something else
        if state == 2:
            courseCtList.append(course)
        if state == 0:
            print("Nice 选到了一门课：" + course)
            return  # 成功了
    # print courseCtList
    courseTemp = [i for i in courseList if (i not in courseCtList)]
    # print courseTemp
    times = 0
    while True:
        times = times + 1
        # 找出已满的课程
        pattern = ('已满.+?(\"8%\" id=\")(.{0,20})\" align')
        courseYmList = [i[1] for i in re.findall(pattern, text, re.S)]
        # print courseYmList
        # 找出可以选的课程编号
        courseAva = [i for i in courseTemp if (i not in courseYmList)]
        # 选课了
        if len(courseAva) == 0:
            print("第" + str(times) + "次刷新，每门课都选不了..")
        else:
            for course in courseAva:
                (state, text) = postRw(course)
                if state == True:
                    state = checkRwState(text)
                else:
                    state = -1
                if state == 0:
                    print("Nice 选到了一门课：" + course)
                    return
                if state == 1:
                    print("人品不好 眼皮子底下的课被抢了")
        # 刷新人文选课界面
        (state, text) = getData(geturl1, header1, data1)
        if text.count('已选') == 3:  # in case of multi-instances
            print("已经选到一门课了")
            break

        if state == False:
            print("打开课程列表页面失败")
            return

        time.sleep(3)


if __name__ == "__main__":
    print("\n\n\n\n")
    print("===================================================================== ")
    print("                    Seu_Jwc_Fker 东南大学选课助手\n")
    print("     访问 github.com/SnoozeZ/seu_jwc_fker 以了解本工具的最新动态")
    print("===================================================================== ")
    print("请选择模式：")
    print("1. 同院竞争模式：只值守主界面本院的“服从推荐”课程(可选择指定的任意数量课程)")
    print("2. 孤注一掷模式：只值守子界面“人文社科类”中你指定一门课程")
    print("3. 暴力模式：值守子界面“人文社科类”任意一门课程，有剩余就选上")
    # print u"4. 只值守子界面“自然科学与技术科学类”中的指定一门课程（开发中）"
    # print u"5. 输入指定任意门课程的名字并值守（课程类型不限）（开发中）"

    # mode = input(u'\n请输入模式编号(如:1)：')
    # userId = raw_input(u'请输入一卡通号(如:213111111)：')
    # passWord = raw_input(u'请输入密码(如:65535)：')
    # semester = input(u'请输入学期编号(短学期为1，秋季学期为2，春季学期为3)：')
    # inputCaptcha = raw_input(u"是否手动输入验证码？ [y]/n: ")

    # used for exporting to exe. damn you cmd
    mode = eval(input('\n请输入模式编号(如:1)：'))
    semester = eval(input('请输入学期编号(短学期为1，秋季学期为2，春季学期为3)：'))
    inputCaptcha = input("是否手动输入验证码？ [N]/Y: ")

    if inputCaptcha == 'y' or inputCaptcha == 'Y':  # should other cases be considered?
        inputCaptcha = True
    else:
        inputCaptcha = False
    ReadLocalDoc = input("是否读取本地账户信息？ [y]/n: ")
    userId = ""
    passWord = ""

    if ReadLocalDoc == 'n' or ReadLocalDoc == 'N':  # should other cases be considered?
        ReadLocalDoc = False
    else:
        ReadLocalDoc = True
    if ReadLocalDoc == True:
        if os.path.exists('Document.txt'):
            with open('Document.txt', 'r') as LocalDoc:
                lines = LocalDoc.readlines()
                userId = lines[0]
                userId = userId.strip('\n')
                print('Local ID: ' + userId)
                passWord = lines[1]
                print('Local Password: ' + passWord)
        else:
            print("没有找到本地账户信息，请手动输入")
            ReadLocalDoc = False

    if not ReadLocalDoc:
        userId = input('请输入一卡通号(如:213111111)：')
        passWord = input('请输入密码(如:65535)：')
        UpdateLocalDoc = input("是否更新本地账户信息？ [y]/n: ")
        if UpdateLocalDoc != 'n' and UpdateLocalDoc != 'N':  # should other cases be considered?
            with open('Document.txt', 'w') as LocalDoc:
                LocalDoc.write(userId)
                LocalDoc.write('\n')
                LocalDoc.write(passWord)

    ReadLocalLessonList = input("是否读取本地目标课程信息？ [y]/n: ")
    if ReadLocalLessonList == 'n' or ReadLocalLessonList == 'N':  # should other cases be considered?
        ReadLocalLessonList = False
    else:
        ReadLocalLessonList = True

    if ReadLocalLessonList == True:
        if os.path.exists('Lesson.txt'):
            with open('Lesson.txt', 'r') as LocalLes:
                WantedLessonsNameList = LocalLes.readlines()
                for id, ls in enumerate(WantedLessonsNameList):
                    WantedLessonsNameList[id] = WantedLessonsNameList[id].strip('\n')
                print(WantedLessonsNameList)
                UpdateLocalLessonList = input("已找到本地课程信息，是否重新输入课程列表并更新？ [n]/y:")
                if UpdateLocalLessonList == 'y' or UpdateLocalLessonList == 'Y':  # should other cases be considered?
                    while True:
                        WantedLes = input("请输入部分课程名称，输入0结束选择:")
                        if WantedLes != '0':
                            WantedLessonsNameList.append(WantedLes)
                        else:
                            break
                    print(WantedLessonsNameList)
                    with open('Lesson.txt', 'w') as LocalDoc:
                        for lessons in WantedLessonsNameList:
                            LocalDoc.write(lessons + '\n')

        else:
            UpdateLocalLessonList = input("没有找到本地课程信息，是否手动输入课程列表并自动更新？（选否待读取课程列表后手动选择） [y]/n:")
            if UpdateLocalLessonList != 'n' and UpdateLocalLessonList != 'N':  # should other cases be considered?
                while True:
                    WantedLes = input("请输入部分课程名称，输入0结束选择:")
                    if WantedLes != '0':
                        WantedLessonsNameList.append(WantedLes)
                    else:
                        break
                print(WantedLessonsNameList)
                with open('Lesson.txt', 'w') as LocalDoc:
                    for lessons in WantedLessonsNameList:
                        LocalDoc.write(lessons + '\n')

    state = False
    failTimes = 0
    while state == False:
        (state, text, url) = loginIn(userId, passWord, inputCaptcha)

        failTimes += 1
        print('验证码识别失败达到%d次' % failTimes)

    if state == True:
        if 1 == mode:
            Mode1(semester, url)
        if 2 == mode:
            courseName = input('请输入你想值守的人文课名称或者其关键词（如:音乐鉴赏）：')
            # courseName = raw_input(u'请输入你想值守的人文课名称或者其关键词（如:音乐鉴赏）：')  # used for exporting to exe
            try:
                courseName.decode('utf-8')
            except:
                courseName.decode('gbk').encode('utf-8')  # handle the input from cmd
            Mode2(semester, courseName, url)
        if 3 == mode:
            Mode3(semester, url)
    else:
        print("要不试试退出后重启一下本程序？")
    eval(input('按任意键退出'))
    # input(u'按任意键退出')  #used for exporting to exe


def ContinueXuanKe():
    Continue = input("是否继续选课？ [y]/n: ")
    if Continue == 'n' or Continue == 'N':  # should other cases be considered?
        eval(input('按任意键退出'))
        quit()
    print("\n===================================================================== ")
    print("                    Seu_Jwc_Fker 东南大学选课助手\n")
    print("     访问 github.com/SnoozeZ/seu_jwc_fker 以了解本工具的最新动态")
    print("===================================================================== ")
    print("请选择模式：")
    print("1. 同院竞争模式：只值守主界面本院的“服从推荐”课程(可选择指定的任意数量课程)")
    print("2. 孤注一掷模式：只值守子界面“人文社科类”中你指定一门课程")
    print("3. 暴力模式：值守子界面“人文社科类”任意一门课程，有剩余就选上")
    mode = eval(input('\n请输入模式编号(如:1)：'))
    if state == True:
        if 1 == mode:
            Mode1(semester, url)
        if 2 == mode:
            courseName = input('请输入你想值守的人文课名称或者其关键词（如:音乐鉴赏）：')
            # courseName = raw_input(u'请输入你想值守的人文课名称或者其关键词（如:音乐鉴赏）：')  # used for exporting to exe
            try:
                courseName.decode('utf-8')
            except:
                courseName.decode('gbk').encode('utf-8')  # handle the input from cmd
            Mode2(semester, courseName, url)
        if 3 == mode:
            Mode3(semester, url)