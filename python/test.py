# -*- coding: GBK -*-

import os
import shutil   
import re     
import zipfile
import time
import shutil
import subprocess
import sys
from win32gui import *
from python.keyinput.action_key     import Key
from python.keyinput.action_text    import Text
from python.keyinput.window_mgr    import WindowMgr

def execCmd(cmd):
    print "执行命令:"+cmd
    r = os.popen(cmd)
    text = r.readlines()
    r.close()
    return text

def DeApk():
    jdcmd = "lib\jd-gui-0.3.5\jd-gui.exe \"D:\Android\Deapk\dist\FirefoxV24.0\classes.jar\""
    subprocess.Popen(jdcmd) # Success!
    WaitAndFore("Java Decompiler")    
    Key("a-f, s").execute()    
    WaitAndFore("Save")
    time.sleep(0.5)
    action = Key("f4/10:2, c-a, delete") + Text("D:\Android\Deapk\dist\FirefoxV24.0")
    action.execute()
    #+ Key("enter/5:4,y")
    w = WindowMgr()     
    while w._handle == None:
        Key("enter/5").execute()
        time.sleep(0.1)
        w.find_window_wildcard("Save All Sources"+".*")
        sys.stdout.write('.')
    print w._handle
    w = WindowMgr()
    w.find_window_wildcard("Save All Sources"+".*")
    while w._handle != None:
        w.find_window_wildcard("Save All Sources"+".*")
        time.sleep(0.01)
        sys.stdout.write('.')
    print ""
    print "保存完毕"
  #  ListWindows()
    print "执行完毕"

def WaitAndFore(title):
    w = WindowMgr()     
    while w._handle == None:
        w.find_window_wildcard(title+".*")
        time.sleep(0.1)
        sys.stdout.write('.')
    print w._handle    
    w.set_foreground()

titles = set()
def foo(hwnd,nouse):
        #去掉下面这句就所有都输出了，但是我不需要那么多
        #if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            titles.add(GetWindowText(hwnd))
def ListWindows():
    EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    lt.sort()
    print "---------------------------------------------"
    for t in lt:
        print t

if __name__ == "__main__":
    DeApk()
