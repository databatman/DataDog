#! /usr/bin/env python
# -*- coding:utf-8 -*-



import os
import json

# const


class Config(object):
    """
    category: means filename that contains file
              such as Joke is a filefold(./story/joke) that contains joke.json
    """
    def __init__(self, user = 'kairong'):

        self.filename = './configuration/%s/config.json' % user    
        if 'config.json' not in os.listdir('./configuration/%s' % user):
            self.config = {}
        else:
            with open(self.filename, 'r') as f:
                self.config = json.load(f)
            
        
    def judgeIfSended(self, category, key):
        self.config.setdefault(category, [])
        if key in self.config[category]:
            return False
        
        return True    

    
    def updateConfig(self, category, key):
        self._update(category, key)
        with open(self.filename, 'w') as f:
            json.dump(self.config, f)
    
        
    def _update(self, category, key):
        """
        used for update config
        """
        self.config.setdefault(category, [])
        self.config[category].append(key)
        
    def showConfig(self):
        print self.config
        
        
        
        