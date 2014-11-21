#!/usr/bin/python
# Set wx.CheckBox height for Windows & Linux
# so it looks the same on both platforms
import wx

class OptionsFrame(wx.Frame):
  def __init__(self, containerobj , parent=None):
    wx.Frame.__init__(self, parent, -1, "Options",size=(300, 150))
    panel = wx.Panel(self)
    notebook = wx.Notebook(panel)
    self.option = containerobj
    self.tabs = (
          (ConnectionPanel(notebook,self.option),"Proxy"),
          (QueuePanel(notebook,self.option), "Queue"),
                )
    for tab, label in self.tabs:
        notebook.AddPage(tab, label)

    sizer = wx.BoxSizer()
    sizer.Add(notebook, 1, wx.EXPAND)
    panel.SetSizer(sizer)
    self.Center()
    self.Bind(wx.EVT_CLOSE, self.OnClose)
    self.load_all_options()
  def OnClose(self, event):
    ''' Event handler for wx.EVT_CLOSE. '''
    self.save_all_options()
    self.Destroy()
  def load_all_options(self):
    ''' Load tabs options. '''
    for tab, _ in self.tabs:
      tab.load_options()
  def save_all_options(self):
    ''' Save tabs options '''
    for tab, _ in self.tabs:
      tab.save_options()
class ConnectionPanel(wx.Panel):
  def __init__(self, parent,option):
    wx.Panel.__init__(self, parent)
    self.option = option
    self.retries_spinner = wx.SpinCtrl(self, size=(50, -1))
    self.retries_spinner.SetRange(1,20)
    self.proxy_box = wx.TextCtrl(self, size=(220, -1))
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    main_sizer.AddSpacer(10)
    main_sizer.Add(self._create_retries_sizer())
    main_sizer.AddSpacer(10)
    main_sizer.Add(wx.StaticText(self, label='Proxy'), flag=wx.LEFT, border=10)
    main_sizer.AddSpacer(5)
    main_sizer.Add(self.proxy_box, flag=wx.LEFT|wx.EXPAND|wx.RIGHT, border=10)
    self.SetSizer(main_sizer)
  def _create_retries_sizer(self):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.AddSpacer(10)
    sizer.Add(wx.StaticText(self, label='Retries'))
    sizer.AddSpacer(5)
    sizer.Add(self.retries_spinner)
    return sizer
  def load_options(self):
    self.proxy_box.SetValue(self.option.getproxy())
    self.retries_spinner.SetValue(self.option.getretries())
  def save_options(self):
    self.option.setproxy(self.proxy_box.GetValue())
    self.option.setretries(self.retries_spinner.GetValue())
class QueuePanel(wx.Panel):
  '''
  Options frame playlist tab panel.Paramsparent: wx.Panel parent.
  '''
  def __init__(self, parent,option):
    wx.Panel.__init__(self, parent)
    self.max_spinner = wx.SpinCtrl(self, size=(70, 20))
    self.max_spinner.SetRange(0, 999)
    self.option = option
    main_sizer = wx.BoxSizer(wx.VERTICAL)

    main_sizer.AddSpacer(20)
    main_sizer.Add(wx.StaticText(self, label='Max Downloads'), flag=wx.LEFT,border =10)
    main_sizer.AddSpacer(5)
    main_sizer.Add(self.max_spinner, flag=wx.LEFT,border = 10)
    self.SetSizer(main_sizer)
  def load_options(self):
    ''' Load panel options from OptionsHandler object. '''
    self.max_spinner.SetValue(self.option.getq())
  def save_options(self):
    ''' Save panel options to OptionsHandler object. '''
    self.option.setq(self.max_spinner.GetValue())
