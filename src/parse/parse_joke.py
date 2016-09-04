#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, re
import urllib, urllib2
import json

def _parseJokes(page = 1):
    """
    get funny jokes from qiushibaike
    """

    url_24 = "http://www.qiushibaike.com/text/page/%d" % page 
    headers = { 'Connection': 'Keep-Alive', 
               'Accept': 'text/html, application/xhtml+xml, */*', 
               'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3', 
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'} 

    req_24 = urllib2.Request(url_24,headers = headers) 

    opener_24 = urllib2.urlopen(req_24) 

    html_24 = opener_24.read()
    rex = '<div class="content">(.*?)</div>' 
    pattern = re.compile(rex, re.S)
    
    m_24 = re.findall(pattern, html_24)
    m_24 = [x.replace('\n\n', '\n')  for x in m_24]
    m_24 = [x.strip('\n') for x in m_24]
    m_24 = [x.strip('<br/>') for x in m_24]

    m_24 = [x.decode('utf-8') for x in m_24]
    
    return m_24


def updateJokes(page = 1):
    """
    parse page=1's jokes and save into json
    """
    if 'jokes.json' not in os.listdir('./story/joke'):
        os.mknod('./story/joke/jokes.json')
        total_jokes = {}
    else:    
        with open('./story/joke/jokes.json', 'r') as f:
            total_jokes = json.load(f)
    picks = _parseJokes(page)                     # parse jokes

    with open('./story/joke/jokes.json', 'w') as f:
        new_keys = [x[:6] for x in picks]
        for i, new_key in enumerate(new_keys):
            total_jokes[new_key] = picks[i]
        
        json.dump(total_jokes, f, encoding = 'utf-8')


if __name__ == "__main__":
    os.chdir('/home/zkr/pyWorkSpace/For_Majesty/reconstruct')
    updateJokes(1)

