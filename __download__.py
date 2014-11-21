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
import __s_download__
import __link_gen__

'''
Global variables declaration
'''
proxy = None


class DownThread():
  def __init__(self, ind, url, path, animename, resume, container, proxy, first, path1):
    self.down_li = ""
    down_link=None
    if "soul-anime" in url:
      nw_req = requests.get(url, proxies = proxy)
      b = BeautifulSoup(nw_req.content)
      x = b.find_all('div', attrs={'id':'vid'})
      a = BeautifulSoup(str(x[0]))
      x = a.find_all('iframe')
      mirr = 'http://www.soul-anime.net' + x[0]['src']
      print mirr
      try:
        r = requests.get(mirr)
        c = re.findall("'file': 'htt.*,", str(r.content))
        down_link = c[0].split("'")[3]
        resume = True
      except Exception as e:
        print e
        mirrs_link = 'http://www.soul-anime.net' + b.find_all('iframe', attrs = {'id':'mirrors'})[0]['src']
        r = requests.get(mirrs_link, proxies = proxy)
        x = BeautifulSoup(r.content)
        no_mirr = BeautifulSoup(str(x.find_all('div', attrs={'id':'mirrors'})[0]))
        no_mirr = len(no_mirr.find_all('a'))
        new_mirr = ""
        print "[+] Number of mirrors found: "+str(no_mirr)
        for i in range(1, no_mirr + 1, 1):
          try:
            mirr_url = mirr[:-5] + '-' + str(i) + mirr[-5:]
            mirr_req = requests.get(mirr_url, proxies = proxy)
            mirr_b = BeautifulSoup(mirr_req.content)
            mirr_link = mirr_b.find_all('iframe', attrs = {'id':'video'})[0]['src']
            if 'youru' in mirr_link:
             try:
              new_r = requests.get(mirr_link)
              j = re.findall('http://stream.vi[^"]*',new_r.content)
              if not j:
               j=re.findall('http://stream[^"]*',new_r.content)
               down_link = j[0]
               resume = True
               break
             except Exception as e:
              print e
              return None
            elif 'video44' in mirr_link:
              mirr_link_req = requests.get(mirr_link, proxies = proxy)
              mirr_link_content = re.findall("url: 'htt.*,", mirr_link_req.content)[0].split("'")[1]
              down_link = mirr_link_content
              resume = False
              break
            elif 'auengine' in mirr_link:
              try:
                new_r = requests.get(mirr_link,proxies = proxy)
                j = re.findall("http://s[^']*",new_r.content)
                for i in j:
                  if 'mp4' in i:
                    down_link = urllib2.unquote(i)
                    resume = True
                    break
              except Exception as e:
                print e
                return None
            else:
              down_link =None
              print "[!] Link not found or link is broken"
          except Exception as e:
            print e
            down_link =None
            print "[!] Link not found or link is broken"
    self.down_li = down_link


    if "animerush" in url:
      Rush=__link_gen__.RushObject(ind, url, animename, resume, proxy)
      self.down_li=Rush.GetLink()
      resume=Rush.resume


    if self.down_li:
      self.start_download = __s_download__.down(ind, self.down_li, path, animename, resume, container, proxy, first, url, path1)
    else:
      wx.CallAfter(Publisher.sendMessage,'update status',[ind,2])
      container.q.get()
