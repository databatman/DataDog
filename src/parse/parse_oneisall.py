#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, re
import urllib, urllib2
import json

import Queue
from threading import Thread


class Oneisall(Thread):
    def __init__(self, queue_page, queue_word):
        Thread.__init__(self)
        self.queue_page = queue_page
        self.queue_word = queue_word
    
    def run(self):
        while True:
            page = self.queue_page.get()
            name, word = self._parseOneisall(page)
            self.queue_word.put((name, word))
            self.queue_page.task_done()
            
            
    def _parseOneisall(self, page):
        """
        get funny jokes from qiushibaike
        """
    
        url = "http://wufazhuce.com/one/%d" % page 
        headers = { 'Connection': 'Keep-Alive', 
                   'Accept': 'text/html, application/xhtml+xml, */*', 
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'} 
    
        req = urllib2.Request(url,headers = headers) 
        opener = urllib2.urlopen(req) 
        html = opener.read()
        rex = '<div class="one-imagen">.*?<img src="(.*?)" alt=.*?<div class="one-titulo">[\s]*(.*?)[\s]*</div>.*?<div class="one-cita">[\s]*(.*?)[\s]*</div>' 
        pattern = re.compile(rex, re.S)
        m = re.findall(pattern, html)
        m = m[0]
        #m0:pic url, m1:name, m2:word
        #name
        name = ''.join(m[1].split('.'))
        #img    
        req = urllib2.Request(m[0], headers = headers)
        opener = urllib2.urlopen(req)
        img = opener.read()
        with open('./picture/onePic/' + name + '.jpg', 'wb') as f:
            f.write(img)
        #word
        word = m[2]
        return name, word
        
def save(queue):      
    if 'one.json' not in os.listdir('./picture/onePic/text') or os.path.getsize('./picture/onePic/text/one.json') == 0:
        f = open('./picture/onePic/text/one.json', 'w')
        f.close()
        one_dict = {}
    else:
        with open('./picture/onePic/text/one.json', 'r') as j:
            one_dict = json.load(j)
        
    while True:
        name, word = queue.get()
        with open('./picture/onePic/text/one.json', 'w') as j:   
            one_dict[name] = word
            json.dump(one_dict, j)
    
        queue.task_done()


class Page(Thread):
    def __init__(self, start_, end, queue):
        Thread.__init__(self)
        self.queue = queue
        self.start_ = start_
        self.end = end
    
    def run(self):
        for i in range(self.start_, self.end):
            self.queue.put(i)

if __name__ == "__main__":
    os.chdir('/home/zkr/pyWorkSpace/For_Majesty/reconstruct')
#    updateOnePic(1)
    queue_page = Queue.Queue()
#    for x in range(35, 1030):
#        queue_page.put(x)
    page = Page(200, 300, queue_page)
    print 1
    page.setDaemon = True
    page.start()
    
    queue_word = Queue.Queue()
    
    for i in range(4):
        work = Oneisall(queue_page, queue_word)
        work.setDaemon = True
        work.start()
        
    save(queue_word)

    queue_page.join()
    queue_word.join()

#    f = open('./picture/onePic/text/a.txt', 'w')
#    g = open('./picture/onePic/text/a.txt', 'w')
#    f.write('testf')
#    g.write('testg')
#    f.close()
#    g.close()
#

