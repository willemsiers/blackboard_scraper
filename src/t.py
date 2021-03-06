#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     04-03-2017
# Copyright:   (c) User 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


from tkinter import *
import tkinter
import tkinter.messagebox
import _thread
import webbrowser
from tkinter.filedialog import askdirectory
from bs4 import BeautifulSoup
import os
import requests
import urllib.request, urllib.error, urllib.parse
import datetime
import base64
import string
import getpass
import multiprocessing
import functools
from io import open as iopen
from urllib.parse import urlsplit
import platform




valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
#sanitizes the filenames for windows (and hopefully other OS' too!)
def sanitize(filename):
    filename = ''.join(c for c in filename if c in valid_chars)
    try:
        while ((filename[len(filename)-1] == ' ') or (filename[len(filename)-1] == '.')):
            filename = filename[:-1]
    except IndexError:
        if len(filename) < 1:
            return 'file_' + filename
        else:
            return filename
    return filename






#class for scraping iLectures from echo360.
class ILectureUnit():
    def __init__(self, link, name):
        print(('ILectureUnit.__init__() link: {link!r}, name:  {name!r}'.format(link=link, name=name)))
        self.link = link
        self.name = name
        self.session = requests.Session()

    # WARMING: Will skip any items without a file box. This has been known to occur for audio-only items.
    #scrapes iLectures from a particular rss feed
    #path: path of the root unit directory
    @staticmethod
    def scrape_ilectures(url, path):
        print(('ILectureUnit.scrape_ilectures() url: {url!r}, path:  {path!r}'.format(url=url, path=path)))
        session = requests.Session()
        request = session.get(url)
        soup = BeautifulSoup(request.text, "html.parser")
        with open('request.text.txt', 'wb') as f:
            f.write(request.text)

        # New
        # Find lectures
        found_lecs = []
        dir = 'iLectures'
        unit_name = soup.title.string
        items = soup.find_all('item')
        for current_item in items:
            print(('current_item: {0!r}'.format(current_item)))
            lec = {}
            try:
                lec['file_url'] = current_item.find('enclosure').get('url')
                lec['date'] = current_item.find('pubdate').text
                lec['title'] = current_item.find('title').text
                found_lecs.append(lec)
            except AttributeError as err:
                print(('Problem parsing item. Skipping it. current_item: {0!r}'.format(current_item)))
                print(('err: {0!r}'.format(err)))
            continue
        # Download lectures
        for lec in found_lecs:
            dirty_filename = '{0} - {1}'.format(lec['date'], lec['title'])
            clean_filename = sanitize(dirty_filename)
            ILectureUnit.fetch_video(lec['file_url'], dir, unit_name, clean_filename, path)
        # /New
##        # Old
##        alist = []
##        blist = []
##        title_list = []
##        dir = 'iLectures'
##        unit_name = soup.title.string
##        for link in soup.find_all('pubdate'):
##            strin = link.string[:-6]
##            alist.append(strin)
##        for title in soup.find_all('title'):
##            strin = link.string[:-6]
##            title_list.append(title.text)
##        for link in soup.find_all('enclosure'):
##            blist.append(link.get('url'))
##        ii = 0
##        for jj in alist:
##            filename = '{0}.{1}'.format(jj, title_list[ii+1])
##            ILectureUnit.fetch_video(blist[ii], dir, unit_name, filename, path)
##            ii = ii + 1
##        # /Old

    #downloads a single iLecture video
    #file_url: the url of the video
    #directory: the directory to save to
    #unit_name: the name of the unit
    #file_name: the name of the video
    #path: root directory to save in
    @staticmethod
    def fetch_video(file_url, directory, unit_name, file_name, path):
        print(('ILectureUnit.fetch_video() directory: {directory!r}, unit_name:  {unit_name!r}, file_name:  {file_name!r}, path:  {path!r}'.format(directory=directory, unit_name=unit_name, file_name=file_name, path=path)))
        #return
        session = requests.Session()
        file_name = string.replace(file_name, ':', '-')
        if '.' in file_name:
            format = '.' + file_name.split('.')[1]
        else:
            format = ' '
        while len(format) > 7:
            format = '.' + file_name.split('.')[1]
        while len(directory) > 50:
            directory = directory[:-1]
        directory = string.replace(directory, ':', '-')
        unit_name = string.replace(unit_name, ':', '-')
        thepath = path + '/' + unit_name + '/' + directory + '/'
        while len(thepath + file_name) > 256:
            file_name = file_name[:-9] + format
        if not os.path.isdir(thepath):
            os.makedirs(thepath)
        if not os.path.exists(path + file_name):
            print(('fetch_video() file_url: {0!r}'.format(file_url)))
            return# REMOVEME
            i = session.get(file_url)
            if i.status_code == requests.codes.ok:
                with iopen(thepath + file_name + '.m4v', 'wb') as file:
                    file.write(i.content)
            else:
                return False



### ILectureUnit.fetch_video() directory: 'iLectures', unit_name:  u'Human Structure and Function 100-ONGOING_313391_LR', file_name:  u'Tue, 28 Feb 2017 15:07:35', path:  '.'
##lecture_unit.fetch_video(
##    file_url,
##    directory,
##    unit_name,
##    file_name,
##path
##)

def main():
    pass

if __name__ == '__main__':
    main()
