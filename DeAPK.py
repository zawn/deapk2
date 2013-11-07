# -*- coding: GBK -*-

import os
import shutil   
import re     
import zipfile
import time
import shutil
import subprocess
import sys
import traceback
import thread
import threading
from python.keyinput.action_key     import Key
from python.keyinput.action_text    import Text
from python.keyinput.window_mgr     import WindowMgr
from python.key_open_window     import KeyOpenWindows

ISOTIMEFORMAT="%Y-%m-%d %X"

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    currentDir = os.path.dirname(sys.executable)
else:
    currentDir = sys.path[0]
os.chdir(currentDir)
apktool_bat =   currentDir+"\\lib\\apktool1.5.1\\apktool.bat"
dex2jar_bat =   currentDir+"\\lib\\dex2jar-0.0.9.13\\d2j-dex2jar.bat"
jd_gui_exe  =   currentDir+"\\lib\\jd-gui-0.3.5\\jd-gui.exe"
apk_dir     =   currentDir+"\\apk"
logdir      =   currentDir+"\\dist"
distdir     =   currentDir+"\\dist"
event       =   threading.Event()
isExt       =   False
zhang = False
prewait = False


def execCmd(cmd):
    print "执行命令:"+cmd
    r = os.popen(cmd)
    text = r.readlines()
    r.close()
    for f in text:
        print f
    return text

def getAPK():
    files = os.listdir(apk_dir);
    results = []
##    print len(files)
    for apkfile in files:
        sufix = os.path.splitext(apkfile)[1]
        if sufix == ".apk":
            results.append(apkfile)
    return results

def WaitAndFore(title):
    w = WindowMgr()     
    while w._handle == None:
        w.find_window_wildcard(title+".*")
        time.sleep(0.1)
        sys.stdout.write('.')
#    print w._handle    
    w.set_foreground()

def subProcess(cmd):
    proc = subprocess.Popen(cmd, stdout = subprocess.PIPE , stderr=subprocess.STDOUT)
    while True:
        #print isPrintWait
        startWait()
        printWaitTime = time.time()
        line = proc.stdout.readline()
        if not line:
            printWaitTime = -1
            endWait()
            break
        endWait()
        print('->' + line.strip())
    proc.wait()
    
def startWait():
    global zhang
    global prewait
    if zhang == True :
        endWait(False) 
    zhang = True
    prewait = False
    event.set()
			
    
            
def endWait(newline = True):
    global zhang
    #print "zhang =+" +str(zhang)
    if zhang :
        event.clear()
        zhang = False
    if prewait and newline:
        print ""
        
def stopWait():
    event.set()
    global isExt
    isExt = True    
    time.sleep(0.15)

class printWaitClass(threading.Thread):
    def __init__(self,event):
        threading.Thread.__init__(self)
        self.threadEvent = event
    def run(self):
        global prewait
        t = -1
        i= 10
        while not isExt:
            #sys.stdout.write('~')
            if t == -1:
                  t = time.time()
            if  self.threadEvent.isSet():
                i=i-1
                if i == 0:
                    if time.time() - t > 1.5:
                        sys.stdout.write('.')
                        prewait = True
                    i=10               
                time.sleep(0.001)
            else:
                t = -1
                self.threadEvent.wait()
        print "End"

wt = printWaitClass(event)
   
def decompileApk(distdir,apkfilename,logdir):
    distApkDir = distdir+ os.sep +os.path.splitext(apkfilename)[0]
    print "Apk文件:"+apkfilename
    print "结果目录:"+distApkDir
    cmdapktool = apktool_bat + " d -s -f -b \""+ apk_dir + os.sep + apkfilename +"\" \""+distApkDir+"\""
    print "正在进行:"+cmdapktool
    # text =  execCmd(cmdapktool)
    subProcess(cmdapktool)
    cmddex2jar = dex2jar_bat + " -f "+"\""+ distApkDir+ os.sep + "classes.dex"+"\""+" -o "+"\""+distApkDir+ os.sep +"classes.jar"+"\""+" -e "+"\""+distApkDir+ os.sep +"classes_error.zip"+"\""
    print "正在进行:"+cmddex2jar
    # text =  execCmd(cmddex2jar)
    subProcess(cmddex2jar)
    jdcmd = jd_gui_exe + " "+"\""+distApkDir+ os.sep +"classes.jar"+"\""
    print "正在进行:打开Java Decompiler"
    subprocess.Popen(jdcmd) # Success!
    setText("")
    WaitAndFore("Java Decompiler")
    def verify1():
        time.sleep(0.1)
        return getText() == "classes.src.zip"
    k1 = KeyOpenWindows("Save",Key("a-t, a-n, c-a,c-c"),verify1,5,1,"确认另存为对话框")
    k2 = KeyOpenWindows("Java Decompiler",Key("a-f, s"),k1.openwindows,5,1,"打开另存为对话框")
    k2.openwindows()
    time.sleep(0.1)
    setText(distApkDir+ os.sep)
    #print "\n正在另存为"+distApkDir+ os.sep+"src.zip"
    k1 = KeyOpenWindows("Save",Key("a-t, a-n, c-a, delete") + Text("src.zip"),"Save",5,1,"重命名为文件为src.zip")
    k1.openwindows()
    k2 = KeyOpenWindows("Save",Key("a-t, a-d, c-a, delete,c-v,a-s,y"),"Save All Sources",5,1,"修改文件路径并保存")
    k2.openwindows()
    print "\nJava Decompiler 正在保存源码,请勿取消! "
    w = WindowMgr()
    w.find_window_wildcard("Save All Sources"+".*")
    abc=1
    while w._handle != None:
        w.find_window_wildcard("Save All Sources"+".*")
        time.sleep(0.01)
        if abc == 1:
            sys.stdout.write('.')
            abc = 10
        else:
            abc = abc - 1
    print "\n保存完毕,正在退出Java Decompiler"
    w = WindowMgr()
    w.find_window_wildcard("Java Decompiler"+".*")
    if w._handle != None:
        w.set_foreground()
        Key("a-x").execute()
    else:
        print "未发现Java Decompiler"
    print "正在解压到"+distApkDir+ os.sep+"src"+os.sep
    zipFile = zipfile.ZipFile(distApkDir+ os.sep+"src.zip")
    #zipFile.extractall(distApkDir+ os.sep+"src")
    startWait()
    for f in zipFile.namelist():
        if f.endswith('/'):
            os.makedirs(distApkDir+ os.sep+"src"+os.sep +f)
        else:
            try:
                zipFile.extract(f,distApkDir+ os.sep+"src")
            except IOError,e:
                traceback.print_exc()
                traceback.print_exc(file=open(logdir+"\\log.txt","a+"))           
    zipFile.close()
    endWait()
    print apkfilename+"处理完毕\n"
    return jdcmd

def main(args):
    wt.start()
    starttime = time.time()
    print("开始时间:"+time.strftime( ISOTIMEFORMAT, time.localtime(starttime) )+"\n")
    apks = getAPK()
    if len(apks)>0 :        
##       print("上级目录:"+os.path.abspath(os.pardir )+"\n")
        print("当前目录:"+currentDir)
        if len(args) == 2:
            global apk_dir
            global logdir
            global distdir
            apk_dir = os.path.dirname(args[1])
            apks = [os.path.basename(args[1])]
            logdir      =   apk_dir+"\\dist"
            distdir     =   apk_dir+"\\dist"
            print("APK文件:"+args[1])
        else:
            print("APK目录:"+apk_dir)
        print("结果目录:"+distdir)
        if os.path.exists(distdir):
            startWait()
            #shutil.rmtree(distdir)
            i=0
            while True:
                print distdir+"_old_"+str(i)
                if os.path.exists(distdir+"_old_"+str(i)):
                    i=i+1
                else:
                    os.rename(distdir,distdir+"_old_"+str(i))
                    break
            endWait()
        os.makedirs(distdir)       
        print("日志目录:"+logdir+"\n")
        if os.path.exists(logdir):
            shutil.rmtree(logdir)
        os.makedirs(logdir)
        log = open(logdir+"\\log.txt","a+")
        i = 0
        length =  len(apks)
        arr =[]
        print("即将处理:")
        for f in apks:
            i = i +1
            print str(i)+"/"+str(length)+" "+f+" \n             ("+apk_dir+ os.sep+f+")"
        i = 0
        print("\n正在处理:")
        for f in apks:
            i = i +1
            print str(i)+"/"+str(length)
            arr.append(decompileApk(distdir,f,logdir))
        for f in arr:
            print("为你打开:"+f)
            time.sleep(0.15)
            subprocess.Popen(f)            
        endtime = time.time()
        print("结束时间:"+time.strftime( ISOTIMEFORMAT, time.localtime(endtime)))
        print "耗时:"+str(int((endtime-starttime)/60))+"分"+str(int((endtime-starttime)%60))+"秒"
        print("结果目录:"+distdir)
        log.close()
    else:
        print("没有找到任何APK文件,在目录:\""+ apk_dir +"\"\n请将需要反编译.apk文件放入上面的目录中.")
    stopWait()
    raw_input("Press any key to exit")

import win32clipboard as w  
import win32con 

def getText():  
    w.OpenClipboard()  
    d = w.GetClipboardData(win32con.CF_TEXT)  
    w.CloseClipboard()  
    return d 

def setText(aString):  
    w.OpenClipboard()  
    w.EmptyClipboard()  
    w.SetClipboardData(win32con.CF_TEXT, aString)  
    w.CloseClipboard()
if __name__ == "__main__":
    main(sys.argv)


        
