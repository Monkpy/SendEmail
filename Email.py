# coding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import time
import datetime

# 设置smtplib所需的参数
# 下面的发件人，收件人是用于邮件传输的。
smtpserver = 'smtp.163.com'
port = 465  # 自己添加的适用于本机与服务器--对应最后发送邮件部分
username = 'xxxx@163.com'
password = '密码（163邮箱为授权码）'
sender = 'xxxx@163.com'  # 发送者使用的邮箱
# receiver='XXX@126.com'
# 收件人为多个收件人以‘,’分开
receiver = ['xxxx@163.com']

data = time.strftime('%Y-%m-%d')
subject = data + '报错日志'
# 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
# subject = '中文标题'
# subject=Header(subject, 'utf-8').encode()

# 构造邮件对象MIMEMultipart对象
# 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
msg = MIMEMultipart('mixed')
msg['Subject'] = subject
msg['From'] = 'xxxx@163.com <xxxxx@163.com>'
# msg['To'] = 'XXX@126.com'
# 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
# msg['To'] = ";".join(receiver)
msg['To'] = ''.join(receiver)
msg['Date'] = data

'''
#构造文字内容   
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.baidu.com"    
text_plain = MIMEText(text,'plain', 'utf-8')    
msg.attach(text_plain)    

#构造图片链接
sendimagefile=open(r'D:\pythontest\testimage.png','rb').read()
image = MIMEImage(sendimagefile)
image.add_header('Content-ID','<image1>')
image["Content-Disposition"] = 'attachment; filename="testimage.png"'
msg.attach(image)

#构造html
#发送正文中的图片:由于包含未被许可的信息，网易邮箱定义为垃圾邮件，报554 DT:SPM ：<p><img src="cid:image1"></p>
html = """
<html>  
  <head></head>  
  <body>  
    <p>Hi!<br>  
       How are you?<br>  
       Here is the <a href="http://www.baidu.com">link</a> you wanted.<br> 
    </p> 
  </body>  
</html>  
"""    
text_html = MIMEText(html,'html', 'utf-8')
text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'   
msg.attach(text_html)    

'''
# 判断前一天是否有日志文件生成
try:
    # 构造附件
    to_day = datetime.datetime.now()
    sendfile = open('E:\Log\scrapy_{}_{}_{}.csv'.format(to_day.year, to_day.month, to_day.day-1), 'rb').read()
    text_att = MIMEText(sendfile, 'base64', 'utf-8')
    text_att["Content-Type"] = 'application/octet-stream'
    # 以下附件可以重命名成aaa.txt
    # text_att["Content-Disposition"] = 'attachment; filename="aaa.txt"'
    # 另一种实现方式
    text_att.add_header('Content-Disposition', 'attachment', filename='bug.csv')
    # 以下中文测试不ok
    # text_att["Content-Disposition"] = u'attachment; filename="中文附件.txt"'.decode('utf-8')
    msg.attach(text_att)
except:
    # 构造文字内容
    text = "小哥很棒昨天没有BUG---再接再厉！！！"
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

# 发送邮件
smtp = smtplib.SMTP_SSL(smtpserver, port)  # 不同于网上的，可以同时应用于服务器部署
# smtp.connect('smtp.163.com')  # 原网上代码，只适用于windows本机
# 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
smtp.set_debuglevel(1)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()

