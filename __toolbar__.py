#!/usr/bin/python
import wx

def init_toolbar(self):
  toolbar = self.CreateToolBar()
  toolbar.AddSeparator()
  play = toolbar.AddLabelTool(wx.ID_ANY,'Start Downloads',wx.Bitmap('Icons/play.png'))
  toolbar.AddSeparator()
  stop = toolbar.AddLabelTool(wx.ID_ANY,'Stop Downloads',wx.Bitmap('Icons/pause.png'))
  toolbar.AddSeparator()
  deleteitems = toolbar.AddLabelTool(wx.ID_ANY,'Remove Items',wx.Bitmap('Icons/recycle.png'))
  toolbar.AddSeparator()
  proxy = toolbar.AddLabelTool(wx.ID_ANY,'Proxy',wx.Bitmap('Icons/proxy.png'))
  toolbar.AddSeparator()
  directory = toolbar.AddLabelTool(wx.ID_ANY, 'Directory', wx.Bitmap('Icons/directory.png'))
  toolbar.AddSeparator()
  about = toolbar.AddLabelTool(wx.ID_ANY,'About',wx.Bitmap('Icons/about.png'))
  toolbar.Realize()
  self.Bind(wx.EVT_TOOL, self.OnDirectory, directory)
  self.Bind(wx.EVT_TOOL, self.OnStart, play)
  self.Bind(wx.EVT_TOOL, self.OnStop, stop)
  self.Bind(wx.EVT_TOOL, self.OnProxy, proxy)
  self.Bind(wx.EVT_TOOL, self.OnRecycle, deleteitems)
  self.Bind(wx.EVT_TOOL, self.OnAbout, about)
