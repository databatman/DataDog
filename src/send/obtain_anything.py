# -*- coding: utf-8 -*-

"""
this file can return regular Joke/Pic/Word that suitable for putting in email
"""
import json
import random

def Jokes():
    """
    iteration to get joke    
    """
    filename = './story/joke/jokes.json'
    with open(filename, 'r') as f:    
        jokes = json.load(f)
    
    keys = jokes.keys()
    random.shuffle(keys)
    for key in keys:
        yield key, jokes[key]            
    


def test():
    a = range(1000, 2000)
    for i, j in enumerate(a):
        yield i, j