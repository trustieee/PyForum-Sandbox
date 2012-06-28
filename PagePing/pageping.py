# Script: pageping.py
# Purpose: Continually checks the status of a given URL.

import wx # for the taskbar icon (http://wxpython.org/download.php#stable)
from subprocess import Popen, PIPE # for executing a process (in our case, ping.exe)
import re # for matching the packets lost in a ping command
import sys


DEBUG = True # toggle this to false if this is running in a production environment

try:
    page = sys.argv[1]
except IndexError:
    page = 'google.com'

PING_COUNT = 1
POLL_TIME = 60*1000 # seconds

if DEBUG:
    POLL_TIME = 5*1000 # seconds

class MyTaskBarFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)

        # timer and taskbaricon
        self.timer = wx.Timer(self)
        self.tbIcon = wx.TaskBarIcon()

        # icons...
        # default:
        self.iconDefault = wx.Icon('icon_pass.jpg', wx.BITMAP_TYPE_JPEG)
        # good
        self.iconSuccess = wx.Icon('icon_succeed.jpg', wx.BITMAP_TYPE_JPEG)
        # bad
        self.iconFail = wx.Icon('icon_fail.jpg', wx.BITMAP_TYPE_JPEG)

        msg = 'Checking status of {0}...'.format(page)
        self.tbIcon.SetIcon(self.iconDefault, msg)

        # event binidngs
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        wx.EVT_TASKBAR_RIGHT_UP(self.tbIcon, self.OnTaskBarRightClick)

        self.timer.Start(POLL_TIME)

    def OnTaskBarRightClick(self, evt):
        self.PopupMenu(self.CreatePopupMenu())

    def OnExitMenuItemClicked(self, evt):
        self.Shutdown()

    def OnTimer(self, evt):
        # ping 'page' 'n' times
        p = Popen("ping.exe {0} -n {1}".format(page, PING_COUNT), stderr=PIPE, stdout=PIPE)

        # store stdout/stderr results in tuple
        (out, err) = p.communicate()

        # find packets lost (typically either 0 or 100) and store the number in the first (and only) group (m.group(1))
        m = re.search("\((\d+)\% loss\)", out)
        if m:
            msg = None
            if m.group(1) == '0':
                msg = '{0} is available'.format(page)
                self.tbIcon.SetIcon(self.iconSuccess, msg)
            elif m.group(1) == '100':
                msg = '{0} is down'.format(page)
                self.tbIcon.SetIcon(self.iconFail, msg)
            else:
                msg = 'Checking status of {0}...'.format(page)
                self.tbIcon.SetIcon(self.iconDefault, msg)

    def CreatePopupMenu(self):
        self.menu = wx.Menu()
        exitMenuItem = self.menu.Append(wx.NewId(), "E&xit", "Exits the application.")
        self.Bind(wx.EVT_MENU, self.OnExitMenuItemClicked, exitMenuItem)
        return self.menu

    def Shutdown(self):
        self.timer.Stop()
        self.tbIcon.RemoveIcon()
        sys.exit()


app = wx.App(False)
frame = MyTaskBarFrame()
app.MainLoop()


