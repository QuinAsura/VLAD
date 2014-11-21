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
import __mythread__, __holder__

'''
Global variables declaration
'''
proxy = None


def load_anime_list(acontent, container):
  container.resetalist()
  container.resetflags()
  if not container.anime_list:
    count = 0
    print ("[+] Loading the list...")
    b = BeautifulSoup(acontent)
    anime = b.find_all("div", attrs={'id' : 'list_table'})
    b = BeautifulSoup(str(anime))
    anime = b.find_all('a')
    for i in anime:
      try:
        if i.text != "BACK TO TOP":
          d=i.text;
          container.anime_list[d.lower()] = "http://www.soul-anime.net" + i['href']
      except:
        pass
    page = requests.get("http://www.animerush.tv/anime-series-list/",proxies = proxy)
    anime = set(re.findall("http://www.animerush.tv/anime/[^/]*/",page.content))
    anime = list(anime)
    for j in anime:
      temp = j
      temp = temp.split("/")[-2]
      d = temp.replace("-"," ").lower()
      if d not in container.anime_list.keys():
        container.anime_list[d]=j
    print ("[+] Test 2 Success the list is Downloaded!")
    container.glist_chk = 1
def load_episode_list(check_url, listctrlobj, container):
  print check_url
  container.resetelist()
  container.resetSum()
  container.resetflags()
  if "soul-anime" in check_url:
    r = requests.get(check_url, proxies = proxy)
    b = BeautifulSoup(r.content)
    c = b.find_all("ul", attrs={'class':'side_list'})
    anime = BeautifulSoup(str(c[0]))
    x = anime.find_all("a")
    for i in x:
      if not 'Ova' in i.text:
        k=i.text.split()[-1]
        if k.isdigit():
          wx.CallAfter(Publisher.sendMessage,"update slist",[str(k),i])
        else:
          for s in i.text.split():
            if s.isdigit() and len(s)<4:
              wx.CallAfter(Publisher.sendMessage,"update slist",[str(s),i])
    container.html_code = (b.find_all('div', attrs = {'id':'anime_data'})[0]).text
    v = b.find_all('div', attrs = {'id':'anime_info'})[0]
    v = BeautifulSoup(str(v))
    temp = 'http://www.soul-anime.net'+str(v.img['src'])
    temp_r = requests.get(temp, proxies = proxy).content
    container.BitMapImage = cStringIO.StringIO(temp_r)
    container.gelist_chk=1

  if "animerush" in check_url:
    r = requests.get(check_url,proxies=None)
    b = BeautifulSoup(r.content)
    container.html_code = (b.find_all('div',attrs={'align':'justify'})[0].text)
    s = b.find_all('div',attrs={'class':'episode_list'})
    episode = BeautifulSoup(str(s))
    epi = episode.find_all("a",attrs={'href':True})
    temp = re.findall('http://www.animerush.tv/[^/]*/[^/]*jpg',r.content)[-1]
    temp = requests.get(temp).content
    container.BitMapImage= cStringIO.StringIO(temp)
    for i in reversed(epi):
      if "Coming soon" not in str(i):
        temp=i['href'].split("/")[-2].replace("-"," ").title()
        epi_no = i['href'].split('-')[-1].replace("/","")
        wx.CallAfter(Publisher.sendMessage,"update rlist",[str(epi_no),temp,i])
    container.gelist_chk=1
def progressLdisplay(dialog, container):
  count = 0
  while not container.glist_chk:
    if count<500:
      count = count + 1
    elif count >=2500:
      count +=0.01
    else:
      count = count + 0.1
    dialog.Update(count)
    wx.Sleep(0.01)
  container.resetflags()
  dialog.Destroy()
def progressELdisplay(dialog, container):
  count = 0
  while not container.gelist_chk:
    if count<500:
      count = count + 1
    elif count>750:
      count += 0.001
    else:
      count = count + 0.01
    dialog.Update(count)
    wx.Sleep(0.01)
  container.resetflags()
  dialog.Destroy()
def start(func, *args):
  thread = threading.Thread(target=func, args=args)
  thread.daemon=True
  thread.start()
def producer(sema, list, first, container, animename):
  while True:
    if not container.q.full():
      sema.release()
      sema.acquire()
      for uniq in range(len(list)):
        while True:
          if container.q.full()  :
            continue
          elif first.progresstable.GetItem(list[uniq][0], 3).GetText() == "Queued":
            thread = __mythread__.MyThread(list[uniq][0], list[uniq][1], list[uniq][2],animename, container, first)
            thread.daemon=True
            thread.start()
            print thread,'started sucker'
            container.q.put(thread, True)
            break
      break
    else:
      continue
