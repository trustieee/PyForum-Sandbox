# Script: pageping.py
# Purpose: Continually checks the status of a given URL.

import wx # for the taskbar icon (http://wxpython.org/download.php#stable)
from subprocess import Popen, PIPE # for executing a process (in our case, ping.exe)
import re # for matching the packets lost in a ping command
from time import sleep
import sys
from os import path
import time

DEBUG = True # toggle this to false if this is running in a production environment

try:
    page = sys.argv[1]
except IndexError:
    page = 'google.com'

PING_COUNT = 1
POLL_TIME = 60*1000 # seconds

if DEBUG:
    POLL_TIME = 5*1000 # seconds

class MyTaskBarIcon(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, None)

        # timer and taskbaricon
        self.timer = wx.Timer(self)
        self.tbIcon = wx.TaskBarIcon()

        icon = wx.Icon('TV.jpg', wx.BITMAP_TYPE_JPEG)
        self.tbIcon.SetIcon(icon, 'Right click me!')

        # event binidngs
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        wx.EVT_TASKBAR_RIGHT_UP(self.tbIcon, self.OnTaskBarRight)

        self.timer.Start(POLL_TIME)

    def OnTaskBarRight(self, evt):
        """ Event handler for right clicking on the task bar icon """
        self.timer.Stop()
        self.tbIcon.RemoveIcon()
        sys.exit()

    def OnTimer(self, evt):
        # ping 'page' 'n' times
        p = Popen("ping.exe {0} -n {1}".format(page, PING_COUNT), stderr=PIPE, stdout=PIPE)

        # store stdout/stderr results in tuple
        (out, err) = p.communicate()

        # find packets lost (typically either 0 or 100) and store the number in the first (and only) group (m.group(1))
        m = re.search("\((\d+)\% loss\)", out)
        print m.group(1) # typically yields either 0 or 100

app = wx.App(False)
frame = MyTaskBarIcon(None)
frame.Show(False)
app.MainLoop()


