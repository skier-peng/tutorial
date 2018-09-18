# -*- coding:utf-8 -*-

import sys
import os
import re
import struct
import binascii
import shutil

import chardet
from get_av_info import AV_FILE_ONLINE

def check_file(files):
    for file in files:
        file = FILE_Home(file)
        #print 'file name is %s,type is %s' % (file.full_name, file.file_type)
        if file.file_type == 'unknown':
            print file.file_name
            print file.f_hcode


class FILE_Home:
    def __init__(self,file):
        if os.path.isfile(file):
            self.full_path = file
            self.basename = os.path.basename(file)
            self.file_type = self.__get_type()
            s = repr(self.basename)
            self.file_name = s.encode('gb2312')

            # self.number =self.__get_number()

        else:
            raise IOError('file not found')
    @property
    def type_list(self):
        return {
            "ffd8ff": "JPEG",
            "89504e47": "PNG",
            "0000001B": "avi",
            "52494646": "avi",
            "0000001c": "mp4",
            "00000020": "mp4",
            "000001ba":"mpg",
            "424dce0b":"bmp",
            "64383a61": "torrent",
            '1a45dfa3':'mkv',
        }



    def __bytes2hex(self, bytes):
        num = len(bytes)
        hexstr = u""
        for i in range(num):
            t = u"%x" % bytes[i]
            if len(t) % 2:
                hexstr += u"0"
            hexstr += t
        return hexstr.upper()

    def __get_type(self):
        binfp = open(self.full_path, 'rb')
        first_line = binfp.readline()
        binfp.close()
        magic_number = binascii.b2a_hex(first_line)[0:8]
        if str(magic_number) in self.type_list.keys():
            ftype = self.type_list[str(magic_number)]
        else:
            ftype = None
        return ftype

    def __get_number(self):

        re1 = '.*?'  # Non-greedy match on filler
        re2 = '([a-z]+)'  # Any Single Word Character (Not Whitespace) 1
        re5 = '-'  # Non-greedy match on filler
        re6 = '(\d+)'  # Any Single Digit 1
        rg = re.compile(re1 + re2 + re5 + re6, re.IGNORECASE | re.DOTALL)
        m = rg.search(self.file_name)
        # self.number = m.groups

    def is_useful_dir(self,path):
        count = 0
        if (os.path.isdir(path)):
            for r, ds, files in os.walk(path):
                for file in files:
                    size = os.path.getsize(os.path.join(r, file))
                    count += size
        if count/1024.0/1024.0>100.0:
            return 1
        else:
            return 0


    def _get_neibor(self):
        file_dir = os.path.dirname(self.full_path)
        file_neibours = os.walk(file_dir)
        (path,dirs,files) = file_neibours.next()
        if not dirs:
            return 2,files
        else:
            for dir in dirs:
                if self.is_useful_dir(dir):
                    return 1

            return 0,files

    def _get_avcode(self,name):
        re1 = '((?:[a-zA-Z]+(-)*[0-9_]+))'  # Variable Name 1

        rg = re.compile(re1, re.IGNORECASE | re.DOTALL)
        m = rg.search(os.path.splitext(name)[0])
        if m:
            var1 = m.group(1)
            return var1
        else:
            return None
    @property
    def av_code(self):
        return self._get_avcode(self.file_name)
    def _get_full_name(self):
        if not hasattr(self,'av_info_online'):
            self.av_info_online = AV_FILE_ONLINE(self.av_code)
        if self.av_info_online:
            return self.av_info_online.av_title
        else:
            return None

    def download_picture(self):
        if not hasattr(self,'av_info_online'):
            self.av_info_online = AV_FILE_ONLINE(self.av_code)
        if self.av_info_online:
            self.av_info_online.download(self.new_home)


    def _get_home(self):
        if self._get_avcode(self.file_name) == self._get_avcode(os.path.dirname(self.full_path)):
            return 1
        else:
            return 0
    def make_home(self,root):
        home_name = self._get_full_name()

        if home_name:
            old_home = os.path.dirname(self.full_path)
            print 'the old name is %s' % old_home
            print 'the root name is %s' % root
            if old_home == root:
                new_home = os.path.join(os.path.dirname(old_home), home_name)
            else:
                new_home = os.path.join(os.path.dirname(old_home),home_name)
            print 'the new name is %s' % new_home
            if not os.path.lexists(new_home):
                if self._get_home() == 1:
                    try:
                        os.rename(os.path.dirname(self.full_path),new_home)
                    except WindowsError,ex:
                        print ex
                        print new_home
                else:
                    try:
                        os.mkdir(new_home)
                        shutil.move(self.full_path,new_home)
                    except WindowsError,ex:
                        print ex

                self.new_home = new_home
            else:
                self.new_home = new_home
        else:
            self.new_home=None



if __name__ == "__main__":
    root = u'D:/迅雷下载/'
    for (root,dir,files) in os.walk(root):
        for file in files:
            print 'this file is %s,root is %s' % (file,root)
            full_file =os.path.join(root,file)
            if os.path.exists(full_file):
                av_file = FILE_Home(os.path.join(root,file))
                print 'av file is %s for file %s' % (av_file,file)
                print av_file.file_type
                print av_file.av_code
                if av_file.file_type in ['avi','mp4','mkv'] and av_file.av_code:
                    print 'began to make home for file: %s' % file
                    av_file.make_home(root)
                    if av_file.new_home:
                        print 'av file new home is %s' % av_file.new_home
                        av_file.download_picture()
                    else:
                        continue



