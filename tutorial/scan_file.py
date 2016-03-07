# -*- coding:utf-8 -*-

import os
import chardet
dir = ''H:\Movie\friends 2000\URE 漫画写实系列'''
for a in os.walk(dir):
    print a
    for b in a:
        print type(b)
        if type(b) == type('str'):
            print b.decode('gb2312')
        if type(b) == type(['list']):
            for c in b:
                if type(c) == type('str'):
                    d=  chardet.detect(c)
                    print "##############"
                    print type(d)
                    print "##############"

