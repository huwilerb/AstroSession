#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:05:17 2021

@author: blaise
"""

from config import Config

class Session:
    
    def __init__(self):
        self.config = Config()
        self.session_name = ''
        
    def test(self):
        print('test')