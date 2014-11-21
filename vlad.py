#!/usr/bin/python
'''
Importing The required Modules
'''
import __mythread__, __holder__, __functions__, __episode_frame__, __toolbar__,__optionFrame__
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
########################################################################################################################################################################
def check():
     try:
          r = requests.get("http://www.soul-anime.net/anime-list.html",proxies = proxy)
          dialog = wx.ProgressDialog("Loading List", "Please wait...", maximum = 3000)
          __functions__.start(__functions__.load_anime_list, r.content, container)
          __functions__.progressLdisplay(dialog, container)
     except requests.exceptions.ConnectionError:
          g = wx.MessageBox("[+] Check Internet Connection !", "Error", wx.OK|wx.ICON_ERROR)
          pass
############################################################################################################################################################################
class MyPopupMenu(wx.Menu):
  def __init__(self, parent, inde):
    super(MyPopupMenu, self).__init__()

    self.parent = parent
    self.inde = inde

    start = wx.MenuItem(self, wx.NewId(), 'Start')
    self.AppendItem(start)
    self.Bind(wx.EVT_MENU, self.OnStart, start)

    pause = wx.MenuItem(self, wx.NewId(), 'Pause')
    self.AppendItem(pause)
    self.Bind(wx.EVT_MENU, self.OnPause, pause)

    #delete = wx.MenuItem(self, wx.NewId(), 'Delete')
    #self.AppendItem(delete)
    #self.Bind(wx.EVT_MENU, self.OnDelete, delete)
  def OnStart(self, e):

    if first.progresstable.GetItem(self.inde, 3).GetText() ==  "Paused":
      first.progresstable.SetStringItem(self.inde, 3, "Queued")
    else:
      pass
  def OnPause(self, e):
    first.progresstable.SetStringItem(self.inde, 3, "Paused")
    #def OnDelete(self, e):
    #    first.progresstable.DeleteItem(self.inde)

#######################################################################################################################################################################
class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        style = (wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX |
                 wx.CLIP_CHILDREN)
        wx.Frame.__init__(self, parent, id, title, size = (910,655), style=style)
        Publisher.subscribe(self.update_percent, "update percentage")
        Publisher.subscribe(self.update_status , "update status")

        self.init_gui()
    def init_gui(self):
        self.panel = wx.Panel(self,-1)
        sizer = wx.GridBagSizer(4,10)
        self.dir = ""
        __toolbar__.init_toolbar(self)
        self.anime_searchbox = wx.TextCtrl(self.panel, -1, "", style=wx.TE_PROCESS_ENTER)
        sizer.Add(self.anime_searchbox, (0,0), (1,8), wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)
        self.button1 = wx.Button(self.panel,-1,"search")
        self.Bind(wx.EVT_BUTTON, self.OnSearch, id=self.button1.GetId())
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        sizer.Add(self.button1,(0,8),(1,1), wx.TOP,10)
        self.anime_listbox = wx.ListBox(self.panel, -1, choices=[])
        sizer.Add(self.anime_listbox, (1,0), (22,10), wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        self.load_episodes = wx.Button(self.panel, -1, "Load Episodes")
        sizer.Add(self.load_episodes, (23,5), (1,1), wx.LEFT|wx.BOTTOM|wx.RIGHT|wx.TOP, 12)
        self.Bind(wx.EVT_BUTTON, self.OnLoadEpisodes, id=self.load_episodes.GetId())
        self.progresstable = wx.ListCtrl(self.panel, style = wx.LC_REPORT | wx.LC_HRULES |wx.LC_VRULES)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick)
        self.progresstable.InsertColumn(0, "Name", width=235)
        self.progresstable.InsertColumn(1, "Size", wx.LIST_FORMAT_CENTRE, width=70)
        self.progresstable.InsertColumn(2, "Completion", wx.LIST_FORMAT_CENTRE, width=95)
        self.progresstable.InsertColumn(3,"Status ",width=100)
        sizer.Add(self.progresstable, (0, 10), (23,27), wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, 12)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        self.panel.SetSizer(sizer)
        self.Centre()
        self.Show()
    def OnSearch(self, event):
       if container.anime_list:
        self.anime_listbox.Clear()
        animename = self.anime_searchbox.GetValue().lower()
        print ("[!] Checking for similar names!")
        r = []
        for near_names in container.anime_list:
            if near_names.startswith(animename[0:4]) or near_names.endswith(animename[-4:]):
                r.append(near_names)
        if r:
            for i in r:
                self.anime_listbox.Append(i.title())
    def update_percent(self,mesg):
      try:
        total_size1 = float(mesg.data[1])
        current_size=float(mesg.data[2])
        up_size = (current_size * 100) / total_size1
        up_size = round(up_size,2)
        if up_size>100:
          self.progresstable.SetStringItem(mesg.data[0],2,'NaN')
          self.progresstable.SetStringItem(mesg.data[0],3,'Error')
        else:
          self.progresstable.SetStringItem(mesg.data[0],2, str(up_size) + " %")
      except Exception as e:
        print e
    def OnDirectory(self,e):
      if not self.dir:
        self.dir = wx.DirDialog(self, message='Select Download Directory', defaultPath='./', style=wx.DD_NEW_DIR_BUTTON,pos=wx.DefaultPosition,size=(200,200), name='Download Directory Selection')
        self.dir.ShowModal()
        container.setdirpath(self.dir.GetPath())
        self.dir=None
    def OnClose(self,e):
      if container.q.full():
        dial = wx.MessageDialog(None, 'Multiple files Downloading.Do You Want To Quit', 'Process', wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result=dial.ShowModal()
        if result == wx.ID_OK:
          for idx in range(self.progresstable.GetItemCount()):
            self.progresstable.SetStringItem(idx, 3, "Paused")
          try:
            self.progresstable.DeleteAllItems()
          except Exception as e:
            print e
            pass
          self.Destroy()
        else:
          pass
      else:
        self.Destroy()
    def OnStart(self,e):
      for idx in range(self.progresstable.GetItemCount()):
        if self.progresstable.GetItem(idx,3).GetText() ==  "Paused":
          self.progresstable.SetStringItem(idx, 3, "Queued")
          time.sleep(0.01)
    def OnStop(self,e):
      for idx in range(self.progresstable.GetItemCount()):
        self.progresstable.SetStringItem(idx, 3, "Paused")
    def OnProxy(self,e):
      options_frame = __optionFrame__.OptionsFrame(container,parent=self)
      options_frame.Show()
    def OnRecycle(self,e):
      for idx in range(self.progresstable.GetItemCount()):
       self.progresstable.SetStringItem(idx, 3, "Paused")
      self.progresstable.DeleteAllItems()
    def OnAbout(self,e):
      description = """ VLAD is a cross platform simplistic anime downloader written in WxPython"""
      licence = """ """
      info = wx.AboutDialogInfo()
      info.SetIcon(wx.Icon('Icons/about.png', wx.BITMAP_TYPE_PNG))
      info.SetName('Acnologia Download Manager')
      info.SetVersion('1.0')
      info.SetDescription(description)
      info.SetCopyright('(C) GPL')
      info.SetWebSite('http://VLAD.com')
      info.SetLicence(licence)
      info.AddDeveloper('Quintessence')
      info.AddDeveloper('Sniper')
      info.AddDocWriter('None')
      info.AddArtist('None')
      info.AddTranslator('None')
      wx.AboutBox(info)
    def update_status(self,mesg):
      try:
       if mesg.data[1] == 1:
         self.progresstable.SetStringItem(mesg.data[0],3,'Completed')
       elif mesg.data[1] ==2:
         self.progresstable.SetStringItem(mesg.data[0],3,'No link found')
       elif mesg.data[1] ==3:
	       self.progresstable.SetStringItem(mesg.data[0],3,'Error')
       elif mesg.data[1] ==4:
         self.progresstable.SetStringItem(mesg.data[0],3,'Downloading')
       elif mesg.data[1] ==5:
         self.progresstable.SetStringItem(mesg.data[0],3,'Retry')
      except Exception as e:
        print e
    def OnLoadEpisodes(self, event):
      if first.anime_listbox.GetStringSelection():
        container.resetelist()
        second = __episode_frame__.Load_Episode_Frame(self, -1, str(first.anime_listbox.GetStringSelection()), container, first)
        second.Show()
        second.MakeModal(True)
    def OnRightClick(self, event):
        menu = event.GetIndex()
        print self.panel.ScreenToClient(wx.GetMousePosition())
        self.PopupMenu(MyPopupMenu(self, menu), self.panel.ScreenToClient(wx.GetMousePosition()))
##################################################################################################################################################################################
container = __holder__.Holder()
app = wx.App()
first = MainFrame(None, -1, "V-L-Anime-Downloader (VLAD)")
check()
app.MainLoop()
