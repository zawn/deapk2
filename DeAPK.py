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
from python.key_open_window         import KeyOpenWindows

ISOTIMEFORMAT="%Y-%m-%d %X"

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    currentDir = os.path.dirname(sys.executable)
else:
    currentDir = sys.path[0]
os.chdir(currentDir)
apktool_bat =   currentDir+"\\lib\\apktool-2.0.0rc4\\apktool.bat"
dex2jar_bat =   currentDir+"\\lib\\dex2jar-0.0.9.15\\d2j-dex2jar.bat"
jd_gui_exe  =   currentDir+"\\lib\\jd-gui-0.3.6\\jd-gui.exe"
apk_dir     =   currentDir+"\\apk"
logdir      =   currentDir+"\\dist"
distdir     =   currentDir+"\\dist"
event       =   threading.Event()
isExt       =   False
zhang = False
prewait = False


def execCmd(cmd):
    print "ִ������:"+cmd
    r = os.popen(cmd)
    text = r.readlines()
    r.close()
    for f in text:
        print f
    return text

def getAPK():
    results = []
    if os.path.exists(distdir):
        files = os.listdir(apk_dir);
        
##      print len(files)
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
    print "Apk�ļ�:"+apkfilename
    print "���Ŀ¼:"+distApkDir
    cmdapktool = apktool_bat + " d -s -f \""+ apk_dir + os.sep + apkfilename +"\" -o \""+distApkDir+"\""
    print "���ڽ���:"+cmdapktool
    # text =  execCmd(cmdapktool)
    subProcess(cmdapktool)
    cmddex2jar = dex2jar_bat + " -f "+"\""+ distApkDir+ os.sep + "classes.dex"+"\""+" -o "+"\""+distApkDir+ os.sep +"classes.jar"+"\""+" -e "+"\""+distApkDir+ os.sep +"classes_error.zip"+"\""
    print "���ڽ���:"+cmddex2jar
    # text =  execCmd(cmddex2jar)
    subProcess(cmddex2jar)
    jdcmd = jd_gui_exe + " "+"\""+distApkDir+ os.sep +"classes.jar"+"\""
    print jdcmd
    print "���ڽ���:��Java Decompiler"
    subprocess.Popen(jdcmd) # Success!
    setText("")
    WaitAndFore("Java Decompiler")
    def verify1():
        time.sleep(0.1)
        return getText() == "classes.src.zip"
    k1 = KeyOpenWindows("Save",Key("a-t, a-n, c-a,c-c"),verify1,5,1,"ȷ�����Ϊ�Ի���")
    k2 = KeyOpenWindows("Java Decompiler",Key("a-f, s"),k1.openwindows,5,1,"�����Ϊ�Ի���")
    k2.openwindows()
    time.sleep(0.1)
    setText(distApkDir+ os.sep)
    #print "\n�������Ϊ"+distApkDir+ os.sep+"src.zip"
    k1 = KeyOpenWindows("Save",Key("a-t, a-n, c-a, delete") + Text("src.zip"),"Save",5,1,"������Ϊ�ļ�Ϊsrc.zip")
    k1.openwindows()
    k2 = KeyOpenWindows("Save",Key("a-t, a-d, c-a, delete,c-v,a-s,y"),"Save All Sources",5,1,"�޸��ļ�·��������")
    k2.openwindows()
    print "\nJava Decompiler ���ڱ���Դ��,����ȡ��! "
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
    print "\n�������,�����˳�Java Decompiler"
    time.sleep(0.5)
    w = WindowMgr()
    w.find_window_wildcard("Java Decompiler"+".*")
    if w._handle != None:
        w.set_foreground()
        Key("a-x").execute()
    else:
        print "δ����Java Decompiler"
    print "���ڽ�ѹ��"+distApkDir+ os.sep+"src"+os.sep
    zipFile = zipfile.ZipFile(distApkDir+ os.sep+"src.zip")
    #zipFile.extractall(distApkDir+ os.sep+"src")
    startWait()
    for f in zipFile.namelist():
        if not f.endswith('/'):
            try:
                zipFile.extract(f,distApkDir+ os.sep+"src")
            except IOError,e:
                traceback.print_exc()
                traceback.print_exc(file=open(logdir+"\\log.txt","a+"))           
    zipFile.close()
    endWait()
    print apkfilename+"�������\n"
    return jdcmd

def main(args):
    wt.start()
    starttime = time.time()
    print("��ʼʱ��:"+time.strftime( ISOTIMEFORMAT, time.localtime(starttime) )+"\n")
    print("��ǰĿ¼:"+currentDir)
    if len(args) == 2:
        global apk_dir
        global logdir
        global distdir
        apk_dir = os.path.dirname(args[1])
        apks = [os.path.basename(args[1])]
        logdir      =   apk_dir+"\\dist"
        distdir     =   apk_dir+"\\dist"
        print("APK�ļ�:"+args[1])
    else:
        apks = getAPK()
        print("APKĿ¼:"+apk_dir)
    if len(apks)>0 :        
##       print("�ϼ�Ŀ¼:"+os.path.abspath(os.pardir )+"\n")
        
        print("���Ŀ¼:"+distdir)
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
        print("��־Ŀ¼:"+logdir+"\n")
        if os.path.exists(logdir):
            shutil.rmtree(logdir)
        os.makedirs(logdir)
        log = open(logdir+"\\log.txt","a+")
        i = 0
        length =  len(apks)
        arr =[]
        print("��������:")
        for f in apks:
            i = i +1
            print str(i)+"/"+str(length)+" "+f+" \n             ("+apk_dir+ os.sep+f+")"
        i = 0
        print("\n���ڴ���:")
        for f in apks:
            i = i +1
            print str(i)+"/"+str(length)
            arr.append(decompileApk(distdir,f,logdir))
        for f in arr:
            print("Ϊ���:"+f)
            time.sleep(0.15)
            subprocess.Popen(f)            
        endtime = time.time()
        print("����ʱ��:"+time.strftime( ISOTIMEFORMAT, time.localtime(endtime)))
        print "��ʱ:"+str(int((endtime-starttime)/60))+"��"+str(int((endtime-starttime)%60))+"��"
        print("���Ŀ¼:"+distdir)
        log.close()
    else:
        print("û���ҵ��κ�APK�ļ�,��Ŀ¼:\""+ apk_dir +"\"\n�뽫��Ҫ������.apk�ļ����������Ŀ¼��.")
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


        
