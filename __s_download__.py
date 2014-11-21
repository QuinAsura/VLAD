#!/usr/bin/python
'''
Importing The required Modules
'''
import wx, sys, requests, urllib2, re, os, Queue, platform
from bs4 import BeautifulSoup
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import threading, time
import  cStringIO
import wx.html
from wx.lib.pubsub import Publisher
import __mythread__
'''
Global variables declaration
'''
proxy = None
class down():
  def __init__(self, ind, down_link, path, animename, resume, container, proxy, first, url, path1):
    ext = requests.get(down_link,stream=True)
    first.progresstable.SetStringItem(ind, 1, str(int(ext.headers['content-length'])/(1024*1024)) + " MB")
    ext = ext.headers['content-type'].split('/')[-1].split('-')[-1]
    if ext == 'stream':
      ext = 'mp4'
    os.chdir(container.dirpath)
    if not os.path.isdir(animename):
      os.makedirs(animename)
    if platform.system() == 'Windows':
      path = animename + '\\' + path + '.' + ext
    else:
      path = animename + '/' + path + '.' + ext
    file_present = os.path.isfile(path)
    print file_present
    down_res = requests.get(down_link,stream=True,proxies=proxy)
    total_size = int(down_res.headers['content-length'])
    wx.CallAfter(Publisher.sendMessage,'update status',[ind,4])
    self.start_download(ind, down_link, path, animename, resume, container, proxy, first, file_present, down_res, total_size, url, path1)
  def start_download(self, ind, down_link, path, animename, resume, container, proxy, first, file_present, down_res, total_size, url, path1):
    if file_present and resume == True:
      file_size = os.path.getsize(path)
      cursize =file_size
      headers = {'Range':'bytes=%s-' % (file_size)}
      r = requests.Request('HEAD', down_link)
      r.headers = headers
      req = r.prepare()
      down_res = requests.get(req.url,headers=req.headers,stream=True,proxies=proxy)
      total_size = int(down_res.headers['content-length'])
      total = requests.head(down_link)
      try:
        with open(path,"a+b") as myfile:
        	for buf in down_res.iter_content(chunk_size=512):
        	  if first.progresstable.GetItem(ind, 3).GetText() == "Downloading":
        	    myfile.write(buf)
        	    myfile.flush()
        	    cursize+=512
        	    wx.CallAfter(Publisher.sendMessage,'update percentage',[ind,(total_size+file_size),cursize])

        	  else:
                    if first.progresstable.GetItem(ind, 3).GetText() == "Paused":
                       break   
                    else:
                       print 'deviation'
                       pass
                       #wx.CallAfter(Publisher.sendMessage,'update status',[ind,4])
                       #myfile.close()
                       #self.start_download(ind,down_link,path,animename,resume,container,proxy,first,file_present,down_res,total_size,url,path1)
		       
        	myfile.close()
        if os.path.getsize(path)>=(total_size+file_size):
	        wx.CallAfter(Publisher.sendMessage,'update status',[ind,1])
      except Exception as e:
        print e
        wx.CallAfter(Publisher.sendMessage,'update status',[ind,3])

    else:
      try:
      	if file_present and resume == False:
          os.remove(path)
        cursize = 0
      	with open(path,"a+b") as myfile:
       	 for buf in down_res.iter_content(chunk_size=512):
       	   if first.progresstable.GetItem(ind, 3).GetText() == "Downloading":
       	     myfile.write(buf)
       	     myfile.flush()
       	     cursize+=512
       	     wx.CallAfter(Publisher.sendMessage,'update percentage',[ind,total_size,cursize])

       	   else:
             if first.progresstable.GetItem(ind, 3).GetText() == "Paused":
                break   
             else:
                print 'deviation'
                pass
                wx.CallAfter(Publisher.sendMessage,'update status',[ind,4])
                myfile.close()
                self.start_download(ind,down_link,path,animename,resume,container,proxy,first,file_present,down_res,total_size,url,path1)
                
                
             
       	 myfile.close()
      	if os.path.getsize(path)>=total_size:
          wx.CallAfter(Publisher.sendMessage,'update status',[ind,1])
      except Exception as e:
        print e
        wx.CallAfter(Publisher.sendMessage,'update status',[ind,3])


    print container.q.get(),ind
    if first.progresstable.GetItem(ind, 3).GetText() == "Paused":
      while True:
        time.sleep(1)
        if first.progresstable.GetItem(ind, 3).GetText() == "Queued" and not container.q.full():
          print down_link
          thread = __mythread__.MyThread(ind, path1, url, animename, container, first)
          thread.setDaemon(True)
          thread.start()
          container.q.put(thread, True)
          break
        else:
          continue
