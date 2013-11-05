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
from python.keyinput.window_mgr     import WindowMgr

distApkDir = "D:\Android\Deapk\dist\FirefoxV24.0"

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
    getText()
    print "准备另存为"+distApkDir+ os.sep+"src.zip"
    while getText() != "classes.src.zip":
        WaitAndFore("Save")
        Key("a-t, a-n, c-a,c-c/2").execute()
        sys.stdout.write('.')
        time.sleep(0.1)
    time.sleep(0.1)
    print ""
    setText(distApkDir+ os.sep)
    print "正在另存为"+distApkDir+ os.sep+"src.zip"
    (Key("a-t, a-n, c-a, delete") + Text("src.zip")).execute()    
    time.sleep(0.1)
    Key("a-t, a-d, c-a, delete,c-v,a-s,y").execute()
    w = WindowMgr()
    i=50
    while w._handle == None:
        #Key("enter").execute()
        time.sleep(0.1)
        i = i-1
        w.find_window_wildcard("Save All Sources"+".*")
        sys.stdout.write('.')
    print w._handle
    print "正在保存源码"
    w = WindowMgr()
    w.find_window_wildcard("Save All Sources"+".*")
    while w._handle != None:
        w.find_window_wildcard("Save All Sources"+".*")
        time.sleep(0.01)
        sys.stdout.write('.')
    print ""
    print "保存完毕,正在退出Java Decompiler"
    w = WindowMgr()
    w.find_window_wildcard("Java Decompiler"+".*")
    if w._handle != None:
        w.set_foreground()
        Key("a-x").execute()
    else:
        print "未发现Java Decompiler"
    print "正在解压"
    zipFile = zipfile.ZipFile(distApkDir+ os.sep+"src.zip")
    zipFile.extractall(distApkDir+ os.sep+"src")
    zipFile.close()
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
    lt.sort()
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
