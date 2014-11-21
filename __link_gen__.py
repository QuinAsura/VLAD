#!/usr/bin/python

'''
Importing The required Modules
'''
import wx, sys, requests, urllib2, re, os, Queue
from bs4 import BeautifulSoup
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import threading, time
import  cStringIO
import wx.html
from wx.lib.pubsub import Publisher

'''
Global variables declaration
'''
proxy = None


class RushObject():
  def __init__(self, ind, url,animename,resume,proxy):
    self.ind = ind
    self.url = url
    self.animename = animename
    self.durl = ''
    self.resume=False
    self.proxy = proxy
  def mirror_gen(self):
    mirrorlist=[]
    url = requests.get(self.url)
    bs  = BeautifulSoup(url.content)
    res = bs.find_all('div',attrs={'id':'episodes'})
    res = BeautifulSoup(str(res))
    res = res.find_all('a',attrs={'href':True})
    for i in range(1,len(res),2):
      mirrorlist.append(res[i])
    return mirrorlist
  def link_gen(self):
      res = self.mirror_gen()
      print "Links found:"+str(len(res))
      for i in res:
        url = requests.get(i['href'])
        bs  = BeautifulSoup(url.content)
        bs  = bs.find_all('iframe')
        for i in bs:
          temp = i['src']
          if ('videoweed' in temp) or ('uploadc' in temp)  or ('daily' in temp) or ('novamov' in temp) or ('facebook' in temp) or ('yucache' in temp) or ('sock' in temp):
            pass
          else:
            temp = self.link_selector(temp)
            if temp:
              self.durl = temp
          if self.durl:
            print "[+]Test-4 Successfully Completed found link of ",self.durl,self
            break
      if  not self.durl:
        print "No link found"
  def link_selector(self,temp):
    if re.search('auengine',temp):
      try:
        new_r = requests.get(temp)
        j =re.findall("http://s[^']*",new_r.content)
        for i in j:
          if 'mp4' in i:
            down_link = urllib2.unquote(i)
            self.resume = True
            return down_link
      except Exception as e:
        print e
        return None

    elif re.search('mp4upload',temp):
      try:
        new_r = requests.get(temp)
        j = re.findall("file': '[^']*",new_r.content)[0].split("'")[-1]
        down_link = urllib2.unquote(j)
        self.resume = True
        return down_link
      except Exception as e:
	     print e
	     return None
    elif re.search('youru',temp):
      try:
        new_r = requests.get(temp)
        j = re.findall('http://stream.vi[^"]*',new_r.content)
        if not j:
          j=re.findall('http://stream[^"]*',new_r.content)
          down_link = j[0]
          self.resume = True
          return down_link
      except Exception as e:
        print e
        return None
    elif re.search('drive',temp):
      try:
        new_r = requests.get(temp)
        j=re.findall('file: "[^"]*',new_r.content)
        down_link = j[0].split('"')[-1]
        self.resume = True
        return down_link
      except Exception as e:
        print e
        return None
    elif re.search('videofun',temp):
      try:
        new_r = requests.get(temp)
        j = re.findall('url:.*',new_r.content)
        down_link = j[-1].split('"')[1]
        down_link = urllib2.unquote(down_link)
        self.resume = True
        return down_link
      except Exception as e:
        print e
        return None
    elif re.search('video44',temp):
      try:
        new_r = requests.get(temp)
        j=re.findall("http[^']*mp4",new_r.content)
        down_link = j[0]
        down_link = urllib2.unquote(down_link)
        self.resume = False
        return down_link
      except Exception as e:
	     print e
      return None
    elif re.search('play44',temp):
      try:
        new_r = requests.get(temp)
        j = re.findall("url: 'http://g.*",new_r.content)
        down_link = j[0].split("'")[1]
        down_link = urllib2.unquote(down_link)
        self.resume = True
        return down_link
      except Exception as e:
        print e
        return None
  def GetLink(self):
    self.link_gen()
    return self.durl
