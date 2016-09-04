#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os; 
from send.send_email import EMail



if __name__ == "__main__":
    os.chdir('/home/zkr/pyWorkSpace/For_Majesty/reconstruct')
    
    name = ""
    head_word = u"""%s，你好哇<br/>""" % name
    

    
    
    email = EMail()
    email.addHead(head_word)
    email.addOnePic()

    a = email.addJokes(2)    
    print a    
    email.addTail(u'<br/><br/>')

    email.send()