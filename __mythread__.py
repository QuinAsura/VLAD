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
import __download__

'''
Global variables declaration
'''
proxy = None


class MyThread(threading.Thread):
  def __init__(self, index_epi, path, down_link, animename, container, first, proxy=None):
    threading.Thread.__init__(self)
    self.ind = index_epi
    self.path = path
    self.url = down_link
    self.animename = animename
    self.durl = ''
    self.container = container
    self.resume = False
    self.proxy = proxy
    self.first = first
  def run(self):
    while True:
      if self.first.progresstable.GetItem(self.ind, 3).GetText() == "Queued":
        self.downthread = __download__.DownThread(self.ind, self.url, self.path, self.animename, self.resume, self.container, self.proxy, self.first, self.path)
        break
      else:
        continue
