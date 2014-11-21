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
import __mythread__, __holder__, __functions__

'''
Global variables declaration
'''
proxy = None

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
  def __init__(self, parent):
    wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
    CheckListCtrlMixin.__init__(self)
    ListCtrlAutoWidthMixin.__init__(self)
class Load_Episode_Frame(wx.Frame):
  def __init__(self, parent, id, title, container, first):
    Publisher.subscribe(self.update_slistbox, "update slist")
    Publisher.subscribe(self.update_rlistbox, "update rlist")

    style = (wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX |wx.CLIP_CHILDREN | wx.FRAME_FLOAT_ON_PARENT)
    wx.Frame.__init__(self, parent, id, title, size=(640,570),style=style)
    panel = wx.Panel(self,-1)
    self.first = first
    self.container = container
    sizer = wx.GridBagSizer(4,10)
    dialog1 = wx.ProgressDialog("Loading Episodes", "Please wait....", maximum = 1000,style=wx.PD_SMOOTH)
    self.episode_listbox = CheckListCtrl(panel)
    self.episode_listbox.InsertColumn(0, "#", width=75)
    self.episode_listbox.InsertColumn(1, "Episode Name")
    sizer.Add(self.episode_listbox, (0,14),(22,4), wx.EXPAND|wx.RIGHT|wx.TOP, 12)
    self.checkall = wx.Button(panel, -1, "Check All")
    sizer.Add(self.checkall, (22,14), (1,1), wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.TOP, 12)
    self.Bind(wx.EVT_BUTTON, self.OnCheckAll, id=self.checkall.GetId())
    self.uncheckall = wx.Button(panel, -1, "Uncheck All")
    sizer.Add(self.uncheckall, (22,15), (1,1), wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.TOP, 12)
    self.Bind(wx.EVT_BUTTON, self.OnUncheckAll, id=self.uncheckall.GetId())
    self.download = wx.Button(panel, -1, "Download")
    sizer.Add(self.download, (22,16), (1,1), wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.TOP, 12)
    self.Bind(wx.EVT_BUTTON, self.OnDownload, id=self.download.GetId())
    self.episode_listbox.DeleteAllItems()
    self.container.resetelist()
    check_url = self.container.anime_list[self.first.anime_listbox.GetStringSelection().lower()]
    __functions__.start(__functions__.load_episode_list, check_url, self.episode_listbox, self.container)
    __functions__.progressELdisplay(dialog1, self.container)
    if self.container.BitMapImage:
      BMI=self.container.BitMapImage
      image = wx.BitmapFromImage(wx.ImageFromStream(BMI))
      image = wx.ImageFromBitmap(image)
      image = image.Scale(200,280, wx.IMAGE_QUALITY_HIGH)
      image = wx.BitmapFromImage(image)
      wx.StaticBitmap(panel,-1,image,(8,5))
    htmlwin=wx.html.HtmlWindow(panel,-1,pos=(8,290), size=(260,260))
    htmlwin.SetStandardFonts()
    htmlwin.SetPage(self.container.html_code)
    self.Bind(wx.EVT_CLOSE, self.on_close)
    self.Centre()
    panel.SetSizer(sizer)
  def update_slistbox(self,mesg):
     if mesg:
       index = self.episode_listbox.InsertStringItem(sys.maxint,str(mesg.data[0]))
       self.episode_listbox.SetStringItem(index, 1, mesg.data[1].text)
       self.container.episode_list[index] = (mesg.data[1].text, "http://www.soul-anime.net" + mesg.data[1]['href'])
  def update_rlistbox(self,mesg):
     if mesg:
       index = self.episode_listbox.InsertStringItem(sys.maxint,mesg.data[0])
       self.episode_listbox.SetStringItem(index, 1, mesg.data[1])
       self.container.episode_list[index] = (mesg.data[1], mesg.data[2]['href'])
  def on_close(self, event):
    self.MakeModal(False)
    event.Skip()
  def OnCheckAll(self, event):
    num = self.episode_listbox.GetItemCount()
    for i in range(num):
      self.episode_listbox.CheckItem(i)
  def OnUncheckAll(self, event):
    num = self.episode_listbox.GetItemCount()
    for i in range(num):
      self.episode_listbox.CheckItem(i, False)
  def OnDownload(self, event):
    num = self.episode_listbox.GetItemCount()
    cnt = 0
    lis = []
    for i in range(num):
     if self.episode_listbox.IsChecked(i):
       index1 = self.first.progresstable.InsertStringItem(sys.maxint, str(self.container.episode_list[i][0]))
       self.first.progresstable.SetStringItem(index1, 1, '--')
       self.first.progresstable.SetStringItem(index1, 2, "--")
       self.first.progresstable.SetStringItem(index1, 3, 'Queued')
       lis.append([index1,str(self.container.episode_list[i][0]),str(self.container.episode_list[i][1])])
       cnt +=1
    if cnt:
      print str(self.first.anime_listbox.GetStringSelection()),'Check for thread start'
      p = threading.Thread(target=__functions__.producer,args=(self.container.sema, lis, self.first, self.container, self.first.anime_listbox.GetStringSelection()))
      p.start()
    print "Test-3 Success the number of items selected:"
    self.Close()
