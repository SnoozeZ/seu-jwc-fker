SeuJwcFker
============
###更新记录
0. 2014-05-30 创世，实现同院竞争臭表脸模式
1. 2014-05-31 代码重写，优化交互，实现人文类课程的孤注一掷模式
2. 2014-06-01 实现人文类课程的暴力模式
3. 2014-09-02 将py脚本封装成为.exe格式，方便无python环境的用户使用
1. 2014-12-26 修改学期选择处的一个提示错误： 短学期输入1，秋季学期为2，**春季学期应输入3**

###SeuJwcFker如何使用？
方法一：使用封装好的.exe文件(**不需python环境**)

1. [点击这里](https://github.com/SnoozeZ/seu-jwc-fker/raw/master/seu_jwc_fker.rar)下载工具压缩包
2. 解压下载下来的压缩包，运行其中的"seu_jwc_fker.exe"，然后根据提示操作

方法二：直接使用python脚本

1. 安装Python环境(推荐Python 2.7)
2. [点击这里](https://raw.githubusercontent.com/SnoozeZ/seu-jwc-fker/master/seu_jwc_fker.py)下载脚本，python解释器中运行之，然后根据提示操作


###SeuJwcFker是什么，能实现什么功能？
SeuJwcFker是一个辅助同学们在东南大学选课系统中顺利选课的工具，可以自动值守空闲课程并注册。目前可以实现以下功能：
* 同院竞争臭表脸模式：值守主界面本院的所有“服从推荐”类课程
* 人文孤注一掷模式：只值守子界面“人文社科类”中你指定一门课程
* 人文暴力模式：值守子界面“人文社科类”所有课程，有剩余就选上

###SeuJwcFker还需要改进的地方：
* 支持任意用户指定的一门~~人文社科类~~、自然类课程的值守
* 支持任意门用户指定课程的值守






###其他
本工具遵循 [WTFPL V2](http://www.wtfpl.net/txt/copying/) 协议

***

###What is the SeuJwcFker?
SeuJwcFker is a tool that helps  students in SEU to efficiently regsiter their courses.


###What can it do?
It can help you to login into the course registering system, and register the courses if there are left courses.

###Need to be done:
* Adopt the tech of Captcha Recognition to support more kind of courses.
* Some bugs may exist.

###How to use? 
1. Install Python development environment. Python 2.7 is recommend.
2. Execute *python seu_jwc_fker.py* in your terminal and then follow the instruction.

###License
Licensed under [WTFPL v2](http://www.wtfpl.net/txt/copying/) unless otherwise specified.






