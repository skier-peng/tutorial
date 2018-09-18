# -*- coding:utf-8

import requests
#from lxml import etree
#from io import StringIO,BytesIO
import HTMLParser
import re
from html.parser import HTMLParser
import os
from bs4 import BeautifulSoup
class AV_FILE_ONLINE(object):
    def __init__(self,av_code):
        self.search_url = 'https://javmoo.com/cn/search/'

        self.film_code = av_code
    def get_short_infomation_online(self):
        r = requests.get(self.search_url+self.film_code)
        short_html = r.content
        soup = BeautifulSoup(short_html,'lxml')
        new_href = soup.find_all("a",class_= "movie-box")
        try:
            return new_href[0].get('href')
        except IndexError,ex:
            print '%s with %s' % (new_href,ex)
            return None
    @property
    def full_info_href(self):
        if not hasattr(self,'_full_info_href'):
            self._full_info_href = self.get_short_infomation_online()
        return self._full_info_href


    def get_full_infomation_online(self):
        if self.full_info_href:
            full_html = requests.get(self.full_info_href).content
            self.full_online_info = BeautifulSoup(full_html, 'lxml')
        else:
            self.full_online_info =  None
    @property
    def av_title(self):
        if not hasattr(self,'full_online_info'):
            self.get_full_infomation_online()
        if self.full_online_info:
            return  self.full_online_info.find_all('h3')[0].text
        else:
            return None
    @property
    def av_jpg_url(self):
        if not hasattr(self,'full_online_info'):
            self.get_full_infomation_online()
        if self.full_online_info:
            return self.full_online_info.find_all("a", class_="bigImage")[0].get('href')
        else:
            return None
    @property
    def actress_list(self):
        if not hasattr(self,'full_online_info'):
            self.get_full_infomation_online()
        actress_list = self.full_online_info.findAll(name = 'a',attrs={'class':'avatar-box'})
        return actress_list

    @property
    def is_collection(self):
        if len(self.actress_list)>3:
            return True
        else:
            return False
    @property
    def release_time(self):
        if not hasattr(self,'_md3_info'):
            self._md3_info = self.full_online_info.findAll(name = 'div',attrs={'class':'col-md-3 info'})[0]
        return self._md3_info.contents[3].contents[1]

    @property
    def director(self):
        if not hasattr(self,'_md3_info'):
            self._md3_info = self.full_online_info.findAll(name = 'div',attrs={'class':'col-md-3 info'})[0]
        return self._md3_info.contents[7].contents[2].text

    @property
    def time_span(self):
        if not hasattr(self,'_md3_info'):
            self._md3_info = self.full_online_info.findAll(name = 'div',attrs={'class':'col-md-3 info'})[0]
        return self._md3_info.contents[5].contents[1]

    @property
    def producer(self):
        if not hasattr(self,'_md3_info'):
            self._md3_info = self.full_online_info.findAll(name = 'div',attrs={'class':'col-md-3 info'})[0]
        return self._md3_info.contents[5].contents[1]





    def download(self,save_path):
        try:
            r = requests.get(self.av_jpg_url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            file = save_path+'/%s.jpg' % self.film_code
            if not os.path.exists(file):
                with open(file, 'wb+') as f:
                    f.write(r.content)
                    f.close()
            else:
                print('file exits')
        except Exception,ex:
            print ex
            pass

class film_info(object):
    def __init__(self,movie_list_item):
        self.movie = movie_list_item
    @property
    def main_page_url(self):
        if not hasattr(self,'_movie_url'):
            self._movie_url=self.movie.get('href')
        return self._movie_url
    @property
    def short_jpg_url(self):
        if not hasattr(self,'_short_jpg_url'):
            self._movie_url = self.movie.get('href')
    @property
    def av_code(self):
        if not hasattr(self,'_av_code'):
            self._av_code = self.movie.find('date').getText()
        return self._av_code


    @property
    def full_info(self):
        if not hasattr(self,'_full_info'):
            self._full_info = AV_FILE_ONLINE(self.av_code)
        return self._full_info


class Movie_list_page(object):

    def __init__(self,movie_list_page):
        self.host = 'https://javmoo.com'

        self._url = movie_list_page
        r = requests.get(self._url)
        self.page =  BeautifulSoup(r.content,'lxml')
        self._movie_list = []

    @property
    def movie_list(self):
        list = self.page.find_all("a", class_="movie-box")
        if not len(self._movie_list) == len(list):
            self._movie_list = []
            for list_item in list:
                film = film_info(list_item)
                self._movie_list.append(film)

        return self._movie_list

    @property
    def next_page_url(self):
        if not hasattr(self,'_next_page_url'):
            next_page = self.page.findAll(name='a', attrs={'name': 'nextpage'})
            if not next_page == []:
                self._next_page_url = next_page[0].get('href')
            else:
                self._next_page_url = self._url

        return self.host + self._next_page_url

    @property
    def url(self):
        return self._url



class Actress_album(object):
    def __init__(self,actress):
        self.search_url = 'https://javmoo.com/cn/actresses'
        self._actress_name = actress
        self._page_list = []

    def _get_actress_page_url(self):
        r =requests.get(self.search_url)
        soup = BeautifulSoup(r.content,'lxml')
        actress_list = soup.find_all("a", class_="avatar-box text-center")
        for actress in actress_list:
            if self._actress_name in actress.get_text().strip('\n'):
                return actress.get('href')
    @property
    def first_page(self):
        if not hasattr(self,'_actress_host'):
            self._actress_host = self._get_actress_page_url()
        self._first_page =  Movie_list_page(self._actress_host)
        if self._first_page not in self._page_list:
            self._page_list.append(self._first_page)
        return self._first_page


    @property
    def current_page(self):
        if len(self._page_list) == 0:
            current_page = self.first_page
        else:
            current_page = self._page_list[-1]
        return current_page

    def get_next_page(self):
        if self.current_page.next_page_url != self.current_page.url:
            page  = Movie_list_page(self.current_page.next_page_url)
            self._page_list.append(page)
            return 1
        else:
            return 0

    def get_actress_page_list(self):
        return self._page_list

    def get_all_page(self):
        while self.get_next_page() == 1:
            pass
        return self.get_actress_page_list()

    @property
    def actress_movie_list(self):
        if not hasattr(self,'_movie_list'):
            self.__get_actress_page_list()
        return self._movie_list

if __name__ == '__main__':
    # av_code = 'MNG-029'
    # av = AV_FILE_ONLINE(av_code)
    # print av.av_title
    # av.download('h:/jpg/')
    av_actress = u'JULIA'
    actress = Actress_album(av_actress)
    #actress.get_all_page()
    actress.get_next_page()
    full_info =  actress.get_actress_page_list()[1].movie_list[0].full_info
    print full_info.is_collection
    print full_info.av_title
    print full_info.full_online_info
    print full_info.film_code