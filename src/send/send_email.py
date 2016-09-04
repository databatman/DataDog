#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""
Created on Sun Jun 12 23:28:40 2016

@author: zkr
"""

import sys; sys.path.append('/home/zkr/pyWorkSpace/For_Majesty/reconstruct/src')

import os
import random
import datetime
import json

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
import smtplib
from email import encoders
from email.utils import parseaddr, formataddr
from email.header import Header

# myself
from config import *
from obtain_anything import Jokes
# CONST



def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode('utf-8'), addr))



class EMail(object):
    from_addr = 'databatman@126.com'
    password = 'zkr1991423'
    smtp_server = 'smtp.126.com'
    user_email = {'kairong':'416223027@qq.com',#'krzhou@sjtu.edu.cn',
                  'XXXX':'XXXX@.com'}
    name = ""
    
    def __init__(self, user = 'kairong'):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.load(user)
        # load config of user
        self.config = Config(user)        
        
        self.msg = MIMEMultipart()
        self.msg['from'] = _format_addr("dtaRobot <%s>" % self.from_addr)
        self.msg['to'] = _format_addr("Majesty <%s>" % self.to_addr)
        self.msg['subject'] = Header("%s private service for you" % date, 'utf-8').encode()
        self.count = 1       # count how many things added in email        
        self.pic_count = 0   # count how many pic will add to attachments
        self.html_head = """<html>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <body>"""
        self.head = "<div class='content'>%s，你好哇</div>" % EMail.name
        self.body = ''
        self.tail = "<br/><br/><div class='content'><font size=1><br/><br/>The Official Version of 2.0 now Online...From Chou Lab</font></div>"
        self.html_tail = "</body></html>"
   
    def load(self, user):
        self.from_addr = EMail.from_addr
        self.password = EMail.password
        self.smtp_server = EMail.smtp_server
        self.to_addr = EMail.user_email[user]
       
   
    def addHead(self, word):
        self.head = "<div class='content'>%s</div>" % word
        
    
    def addTail(self, word):
        self.tail = "<div class='content'>%s</div>" % word + self.tail
    
    def addJokes(self, frequent = 6):
        self.body = self.body + "<br/><br/><div class='content'>%s</div>" % u"搞笑段子如下："
        jokes = Jokes()
        self.joke_count = 0
        flags = 0
        for key, word in jokes:
            if flags == frequent:
                break
            flag = self._addJoke(key, word)
            if flag == True:
                flags += 1
        
        return True
    
    
    def _addJoke(self, key, word, kind = 'Joke'):
        flag = self.judge(kind, key)
        if flag == True:
            self.body = self.body + "<div class='content'>%s<br/>%s</div>" % (self.joke_count, word)
            self.count += 1    # put on every add's last
            self.joke_count += 1
            self.update(kind, key)
        else:
            print 'Got a Joke that already read,Please change.'
        return flag
    
    
    
    def randomPic(self, word = '', kind = 'random'):
        """
        """
        kinds = ['longPic', 'onePic']
        ls_kind = []
        for x in kinds:
            ls_kind.append(os.listdir('./picture/%s' % x))
        
        
        for i in range(len(kinds)):
            for one in ls_kind[i]:
                if self.addPic(word, kinds[i], one):
                    return True
        
        return False

  
    def addPic(self, word, kind, picname):
        """
        kind: longPic/onePic/JokePic or anything else
        """
        key = picname.split('.')[0]
        flag = self.judge(kind, key)
        if flag == True:
            self._addAttachment(kind, picname)
            self.body = self.body + """<div class='content'>%s</div><img src="cid:%d"/>""" % (word, self.pic_count)      
            self.pic_count += 1
            self.count += 1    # put on every add's last
            self.update(kind, key)

        else:
            print 'Pic is already read. Please change.'
            return False
            
    def addOnePic(self):
        """
        reuse of addPic
        """
        ls = os.listdir('./picture/onePic')
        random.shuffle(ls)
        for i in range(len(ls)):    
            pickname = ls[i]
            name = pickname.split('.')[0]
            if self.judge('onePic', name):
                break
            
        with open('./picture/onePic/text/one.json', 'r') as f:
            one_dict = json.load(f)
            word = one_dict.setdefault(name, '')
            word = '<br>' + "OneIsAll: " + name + '<br>' + word
        self.addPic(word, 'onePic', pickname)
             

    def addMoive(self, kind, name):
        """
        Ver3.0's function
        """
        key = name.split('.')[0]
        flag = self.judge(kind, key)
        if flag == True:
            pass
        else:
            print 'Movie is already read. Please change.'
            return False
  
        
    def send(self):
        self._mergeHtml()        
        server = smtplib.SMTP(self.smtp_server, 25)
        server.starttls()
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, [self.to_addr], self.msg.as_string())
        server.quit()


    def _mergeHtml(self):
        self.total = self.html_head + self.head + self.body + self.tail + self.html_tail
        self.msg.attach(MIMEText(self.total, 'html', 'utf-8'))
 
    def showHtml(self):
        self.total = self.html_head + self.head + self.body + self.tail + self.html_tail

        print self.total
    
    
    def _addAttachment(self, kind, name):
        """
        kind: such as picture/jokePic
        this is now only for pic, maybe in ver3.0 I can use it to send video
        """
        _filename = './picture/%s/%s' % (kind, name)
        print _filename
        with open(_filename, 'rb') as f:
            mime = MIMEBase('image', 'png', filename = name)
            mime.add_header('Content-Disposition', 'attachment', filename = name)
            mime.add_header('Content-ID', '<%d>' % self.pic_count)
            mime.add_header('X-Attachment-Id', '%d' % self.pic_count)
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            self.msg.attach(mime)        

    def judge(self, kind, key):
        """
        lower the coupling of codes
        """
        flag = self.config.judgeIfSended(kind, key)
        return flag
    
    def update(self, kind, key):
        self.config.updateConfig(kind, key)
    
    
    #with open('/home/zkr/pyWorkSpace/krzhou_CV.pdf', 'rb') as f:
    #           mime = MIMEBase('krzhou_CV_post', 'pdf', filename = 'krzhou.pdf')
    #           mime.add_header('Content-Disposition', 'attachment', filename = 'krzhou.pdf')
    #           mime.add_header('Content-ID', '0')
    #           mime.add_header('X-Attachment', '0')
    #           mime.set_payload(f.read())
    #           encoders.encode_base64(mime)
    #           msg.attach(mime)



if __name__ == "__main__":
    os.chdir('/home/zkr/pyWorkSpace/For_Majesty/reconstruct')
    email = EMail()
    email.addHead(u'试试看这个字体大不大，学下怎么调整字体。')
    a = email.addJokes()    
    print a    
    email.addTail(u'<br/><br/>这里是尾巴尾巴。')
    email.addOnePic()

    email.send()
