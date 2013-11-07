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
from keyinput.action_key     import Key
from keyinput.action_text    import Text
from keyinput.window_mgr     import WindowMgr
from key_open_window     import KeyOpenWindows
import win32process
import win32gui

distApkDir = "D:\Android\Deapk\dist\FirefoxV24.0"

def execCmd(cmd):
    print "执行命令:"+cmd
    r = os.popen(cmd)
    text = r.readlines()
    r.close()
    return text


def DeApk():
    jdcmd = "..\lib\jd-gui-0.3.5\jd-gui.exe \"D:\Android\Deapk\dist\百度浏览器V4.0.7.10\classes.jar\""
    notepad = subprocess.Popen(jdcmd) # Success!
    #WaitAndFore("Java Decompiler")    
   # Key("a-f, s").execute()   
   # WaitAndFore("Save")
    def verify1():
        time.sleep(0.1)
        return getText() == "classes.src.zip"
    k1 = KeyOpenWindows("Save",Key("a-t, a-n, c-a,c-c"),verify1,4,5,"确认另存为对话框")
    k2 = KeyOpenWindows("Java Decompiler",Key("a-f, s"),k1.openwindows,2,1,"打开另存为对话框")

    k2.openwindows()
    
    setText(distApkDir+ os.sep)
    print "\n正在另存为"+distApkDir+ os.sep+"src.zip"
    (Key("a-t, a-n, c-a, delete") + Text("src.zip")).execute() 

    print "\n**-----------------------------"
    ListWindows()
    print "执行完毕"


def WaitAndFore(title):
    w = WindowMgr()     
    while w._handle == None:
        w.find_window_wildcard(title+".*")
        time.sleep(0.1)
        sys.stdout.write('.')
    print w._handle    
    w.set_foreground()
    time.sleep(0.1)

titles = set()
def foo(hwnd,nouse):
        #去掉下面这句就所有都输出了，但是我不需要那么多
        #if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            titles.add(GetWindowText(hwnd))
def ListWindows():
    EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    #lt.sort()
    print "---------------------------------------------"
    for t in lt:
        print t

import win32clipboard
import win32con 
        
def getText():  
    win32clipboard.OpenClipboard()  
    d = win32clipboard.GetClipboardData(win32con.CF_TEXT)  
    win32clipboard.CloseClipboard()  
    return d 

def setText(aString):  
    win32clipboard.OpenClipboard()  
    win32clipboard.EmptyClipboard()  
    win32clipboard.SetClipboardData(win32con.CF_TEXT, aString)  
    win32clipboard.CloseClipboard()

if __name__ == "__main__":
    DeApk()
