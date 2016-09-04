#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os; 
from send.send_email import EMail



if __name__ == "__main__":
    os.chdir('/home/zkr/pyWorkSpace/For_Majesty/reconstruct')
    
    EName = ""
    CName = ""
    head_word = u"""%s，你好哇<br/>目前我的版本是2.0，hoho，新增了以下功能：
    <br/><font size=5>1、图片方面</font>
       <br/>  1.1、以概率<span style="color:#cc0000">p1</span>在邮件最后附上<span style="color:#cc0000">OneIsAll的图文小段子</span>，都是很小清新的话哦，嘿嘿
       <br/>  1.2、以概率<span style="color:#cc0000">q1</span>在邮件最后附上<span style="color:#cc0000">搞笑的长图</span>
       <br/>  1.3、以概率<span style="color:#cc0000">r1</span>在邮件最后附上<span style="color:#cc0000">老大的黑历史图片</span>(笑)
    <br/><font size=5>2、文字方面</font>
       <br/>  2.1、以概率<span style="color:#cc0000">p2</span>附上<span style="color:#cc0000">搞笑段子</span>
       <br/>  2.2、以概率<span style="color:#cc0000">q2</span>附上<span style="color:#cc0000">XXXX相关</span>的知识
       <br/>  2.3、以概率<span style="color:#cc0000">r2</span>附上<span style="color:#cc0000">XXXX相关</span>的知识
       <br/>  2.4、以概率<span style="color:#cc0000">s2</span>附上<span style="color:#cc0000">XXXX相关</span>的知识
       <br/>  2.5、以概率<span style="color:#cc0000">t2附上老大记录过的话</span>(笑，估计没什么市场)
    <br/><br/> 
       """ % CName
    

    
    
    email = EMail(EName)
    email.addHead(head_word)
    email.addOnePic()

    a = email.addJokes(1)    
    print a    
    email.addTail(u'<br/><br/>')

    email.send()
