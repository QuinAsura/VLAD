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


class Holder():
  def __init__(self):
    self.qno = 1
    self.anime_list ={}
    self.episode_list={}
    self.glist_chk = 0
    self.gelist_chk= 0
    self.BitMapImage=0
    self.dlist = []
    self.html_code= "Sorry Broken link"
    self.q = Queue.Queue(self.qno)
    self.sema = threading.Semaphore(1)
    self.retries = 10
    self.proxy   = None
    self.dirpath = './'

  def resetflags(self):
    '''
    Resets the flags used by
    '''
    self.glist_chk=0
    self.gelist_chk=0

  def setdirpath(self,path):
    self.dirpath = path


  def resetSum(self):
    '''
    Resets the image and summary variable
    '''
    self.BitMapImage=0
    self.html_code= "Sorry Broken link"

  def resetalist(self):
    self.anime_list={}

  def resetelist(self):
    self.episode_list ={}

  def resetIm(self):
    self.BitMapImage=0

  def resetdlist(self):
    self.dlist=[]

  def getproxy(self):
    return str(self.proxy)

  def getretries(self):
    return (self.retries)

  def setretries(self,value):
    self.retries = int(value)

  def setproxy(self,value):
    self.proxy = str(value)

  def setq(self,value):
    if self.qno == int(value):
	pass
    else:
	self.qno=int(value)-1
        self.q = Queue.Queue(self.qno)

  def getq(self):
    return (self.qno)
