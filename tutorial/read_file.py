 # -*- coding:utf-8 -*-

import sys
import os
import re
import chardet

def VisitDir(arg,dirname,names):
        for file_name in names:
                #rint dirname
                #rint file_name
                file_list.append(dirname+'/'+file_name)



class av_file:
    def __init__(self,path,file):
        if os.path.exists(os.path.join(path, file)):
            self.full_name = os.path.join(path, file)
            self.file_name = file
            self.file_type = self.__get_type()
            self.number =self.__get_number()
        else:
            return None
    def __get_number(self):

        re1='.*?'	# Non-greedy match on filler
        re2='([a-z]+)'	# Any Single Word Character (Not Whitespace) 1
        re5='-'	# Non-greedy match on filler
        re6='(\d+)'	# Any Single Digit 1
        rg = re.compile(re1+re2+re5+re6,re.IGNORECASE|re.DOTALL)
        m = rg.search(self.file_name)
        print m.groups()
        #self.number = m.groups
    def __get_type(self):

        return

if __name__ == "__main__":
    dir = r'E:\\合计\\搜查官\\'.decode('utf-8')
    for root, dirs, files in os.walk(dir):
        for dir in dirs:
            #print(os.path.join(root, dir))
            pass
        for file in files:
            av = av_file(root,file)
            print av.file_name
            print "the number is ", av.number




