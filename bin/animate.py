#!/usr/bin/python
################################################################################
# Animate class for LED strips
# The goal here is to make far faster animations than are possible by
# calculating each pixel each frame.
################################################################################
# Instantiate passing in a NeoPixel strip object and the name of the animation
# function.
#
# https://stackoverflow.com/questions/19846332/python-threading-inside-a-class
# https://stackoverflow.com/questions/18018033/how-to-stop-a-looping-thread-in-python
################################################################################
from   neopixel import *
import threading
import time
import sys
from neopixel import *
from random import random
import simplejson as json

def runanimation(fn):
  def wrapper(*args, **kwargs):
    thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
    thread.start()
    return thread

  return wrapper

def runshow(anim, name, args=None):
  if name == "Current":
    cs = anim.getcurrentshow()
    #Create args tuple
    tmp = []
    for arg in cs['args']:
      tmp.append(arg['value'])
    args = tuple(tmp)
    name = cs['name']
  func = getattr(anim,name)
  if args == None:
    thd = func()
  else:
    thd = func(*args)
  return thd

class Animate:
  def __init__(self, inifile = '/etc/lightshow/lightshow.json'):
    self.name = "Animate"
    self.inifile = inifile

    with open(inifile, 'r') as configfile:
      self.cfg = json.load(configfile)

    self.colornames = {}
    self.colornames = self.cfg['Colors']

    self.strip = Adafruit_NeoPixel(self.cfg['Strip']['leds'],
                                   self.cfg['Strip']['gpio'],
                                   self.cfg['Strip']['freq'],
                                   self.cfg['Strip']['dma'],
                                   self.cfg['Strip']['invert'],
                                   self.cfg['Strip']['brightness'],
                                   self.cfg['Strip']['chan'],
                                   int(self.cfg['Strip']['strip'],16)
                             )
    self.strip.begin()
    self.pxls = self.strip.numPixels()

  def savecolor(self,name,colval):
    self.colornames[name] = int(colval)
    self.cfg['Colors'] = self.colornames
    with open(self.inifile, 'wb') as configfile:
      configfile.write(json.dumps(self.cfg,indent=2))

  def savecurrentshow(self,showinfo):
    self.cfg['CurrentShow'] = showinfo
    with open(self.inifile, 'wb') as configfile:
      configfile.write(json.dumps(self.cfg,indent=2))

  def getcolors(self):
    carr = []
    for k in self.colornames:
      carr.append(k)
    return sorted(carr)
    
  def getcolor(self, colorname):
    return self.colornames[colorname]
    
  def getcurrentshow(self):
    return self.cfg['CurrentShow']
    
  def asleep(self,sleepfor=1000):
    #Animation sleep ... sleep while still checking for signals
    start = int(round(time.time() * 1000))
    end = start + sleepfor
    #print "Start = " + str(start) + " and end = " + str(end)
    while getattr(self.thread, "running", True) and int(round(time.time() * 1000)) < end:
      time.sleep(10/1000)
    return getattr(self.thread, "running", True)

  @runanimation
  def Solid(self,color="off"):
    showinfo = {"name":"Solid","args":[{"name":"Color","type":"string","value":color}]}
    self.savecurrentshow(showinfo)
    for i in range(self.pxls):
      self.strip.setPixelColor(i,self.colornames[color])
    self.strip.show()

  @runanimation
  def SetPixel(self,p=0,cvar=0):
    if cvar in self.colornames:
      self.strip.setPixelColor(p,self.colornames[cvar])
    else:
      self.strip.setPixelColor(p,cvar)
    self.strip.show()

  @runanimation
  def ColorWipe(self,delay=10,step=2,colors=["red","white","blue"]):
    showinfo = {"name":"ColorWipe","args":[{"name":"Delay","type":"int","value":delay},
                                           {"name":"Step","type":"int","value":step},
                                           {"name":"Colors","type":"colorarray","value":colors}]}
    self.savecurrentshow(showinfo)
    self.thread = threading.currentThread()
    start = 0
    end = self.pxls
    dir = 1
    if step <= 0:
      start = self.pxls
      end = 0
      dir = -1
    while getattr(self.thread, "running", True):
      for i in colors:
        if not getattr(self.thread, "running", True):
          break
        index = start
        for j in range(start,end,step):
          while index != j:
            self.strip.setPixelColor(index,self.colornames[i])
            index += dir
          self.strip.show()
          if not self.asleep(delay):
            return
        if index != end:
          while index != end:
            self.strip.setPixelColor(index,self.colornames[i])
            index += dir
          self.strip.setPixelColor(end,self.colornames[i])
          self.strip.show()

  @runanimation
  def Comet(self,clen=20,delay=100,step=1):
    showinfo = {"name":"Comet","args":[{"name":"Length","type":"int","value":clen},
                                       {"name":"Delay","type":"int","value":delay},
                                       {"name":"Step","type":"int","value":step}]}
    self.savecurrentshow(showinfo)
    self.thread = threading.currentThread()
    comet = []
    colorstep = 255/clen
    for i in range(255,0,-colorstep):
      comet.append(Color(i,i,i))
    for i in range(step):
      comet.append(0)
    clen = len(comet)
    start = 0
    end = self.pxls + clen
    dir = 1
    if step <= 0:
      start = self.pxls
      end = 0
      dir = -1
    index = start
    while getattr(self.thread, "running", True):
      index = start
      cometend = 0
      for j in range(start,end,step):  
        for k in range(clen):
          cp = j-k
          if cp >= 0 and cp < end:
            self.strip.setPixelColor(cp,comet[k])
        self.strip.show()
        if not self.asleep(delay):
          return
      

  @runanimation
  def EveryX(self,skip=1,delay=60000,colors=["red","green"]):
    showinfo = {"name":"EveryX","args":[{"name":"Skip","type":"int","value":skip},
                                        {"name":"Delay","type":"int","value":delay},
                                        {"name":"Colors","type":"colorarray","value":colors}]}
    self.savecurrentshow(showinfo)
    self.thread = threading.currentThread()
    cols = len(colors)
    step = cols + (cols*skip)
    while getattr(self.thread, "running", True):
      for e in range(skip+1):
        if e-1 >= 0:
          self.strip.setPixelColor(e-1,0)
        for i in range(e,self.pxls,step):
          for k in range(cols):
            offset = (k*skip)+k
            self.strip.setPixelColor(i+offset-1,0)
            self.strip.setPixelColor(i+offset,self.colornames[colors[k]])
            for m in range(1,skip):
              self.strip.setPixelColor(i+offset+m,0)
        self.strip.show()
        if not self.asleep(delay):
          return
      c = colors.pop()
      colors.insert(0,c)

