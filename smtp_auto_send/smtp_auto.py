#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#跟着廖雪峰学python

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr

import smtplib, base64

#格式化方法
def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr((Header(name, 'utf-8').encode(), addr))

#你的邮箱	
from_addr = 'abc@163.com'
#你的密码,不想明文保存的话，可以base64decode加盐或md5加盐
password = 'password'
#收件人和抄送列表，第一个为收件人，其余为抄送人
to_addr = ['john@163.com', 'fucker@163.com']
#smtp服务地址
smtp_server = 'smtp.163.com'

msg = MIMEMultipart()
msg['From'] = _format_addr('agaghd<%s>' % from_addr)
msg['To'] = _format_addr('<%s>' % to_addr[0])
#通过循环取抄送人列表
msg['CC'] = ''
i = 1
n = len(to_addr)
while i < n:
	msg['CC'] = msg['CC'] + (_format_addr('<%s>' % to_addr[i]))
	i = i + 1
	if i < n:
		msg['CC'] + (',')

msg['Subject'] = Header('附件', 'utf-8').encode()

#邮件正文是MIME Text：
msg.attach(MIMEText('附件已发送，请查收', 'plain', 'utf-8'))

#添加附件
with open(r'C:\file\abc.txt','rb') as f:
	#设置附件的MIME和文件名，从本地读取：
	mime = MIMEBase('abc', 'txt', filename = 'abc.txt')
	#加上必要的头信息
	mime.add_header('Content-Disposition', 'attachment', filename = 'abc.txt')
	mime.add_header('Content-ID', '<0>')
	mime.add_header('X-Attachment-Id', '0')
	#把附件的内容读进来
	mime.set_payload(f.read())
	#用Base64编码
	encoders.encode_base64(mime)
	#添加到MIMEMultipant：
	msg.attach(mime)
	

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit()