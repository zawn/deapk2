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
from python.keyinput.action_key     import Key
from python.keyinput.action_text    import Text
from python.keyinput.window_mgr     import WindowMgr

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
logdir      =   currentDir+"\\dist_log"
distdir     =   currentDir+"\\dist"


def execCmd(cmd):
    print "执行命令:"+cmd
    r = os.popen(cmd)
    text = r.readlines()
    r.close()
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
    
def decompileApk(distdir,apkfilename,logdir):
    distApkDir = distdir+ os.sep +os.path.splitext(apkfilename)[0]
    print "Apk文件:"+apkfilename
    print "结果目录:"+distApkDir
    text =  execCmd(apktool_bat + " d -s -f -b \""+ apk_dir + os.sep + apkfilename +"\" \""+distApkDir+"\"")
    for f in text:
        print f
    text =  execCmd(dex2jar_bat + " -f "+"\""+ distApkDir+ os.sep + "classes.dex"+"\""+" -o "+"\""+distApkDir+ os.sep +"classes.jar"+"\""+" -e "+"\""+distApkDir+ os.sep +"classes_error.zip"+"\"")
    for f in text:
        print f
    jdcmd = jd_gui_exe + " "+"\""+distApkDir+ os.sep +"classes.jar"+"\""
    print "正在打开Java Decompiler"
    subprocess.Popen(jdcmd) # Success!
    WaitAndFore("Java Decompiler")    
    Key("a-f, s").execute()
    print "\n正在打开另存为对话框"
    WaitAndFore("Save")
    setText("None")
    print "\n确认另存为对话框状态"
    while getText() != "classes.src.zip":
        WaitAndFore("Save")
        Key("a-t, a-n, c-a,c-c/2").execute()
        sys.stdout.write('.')
        time.sleep(0.1)
    setText(distApkDir+ os.sep)
    print "\n正在另存为"+distApkDir+ os.sep+"src.zip"
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
    print "\nJava Decompiler 正在保存源码,请勿取消! "
    w = WindowMgr()
    w.find_window_wildcard("Save All Sources"+".*")
    abc=1
    while w._handle != None:
        w.find_window_wildcard("Save All Sources"+".*")
        time.sleep(0.01)
        if abc == 1:
            sys.stdout.write('.')
            abc = 4
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
    print apkfilename+"处理完毕\n"
    return jdcmd

def main():
    starttime = time.time()
    print("开始时间:"+time.strftime( ISOTIMEFORMAT, time.localtime(starttime) )+"\n")
    apks = getAPK()
    if len(apks)>0 :        
##       print("上级目录:"+os.path.abspath(os.pardir )+"\n")
        print("当前目录:"+currentDir+"\n")
        print("APK目录:"+apk_dir +"\n")
        print("结果目录:"+distdir+"\n")
        if os.path.exists(distdir):
            shutil.rmtree(distdir)
        os.makedirs(distdir)       
        print("日志目录:"+logdir+"\n")
        if os.path.exists(logdir):
            shutil.rmtree(logdir)
        os.makedirs(logdir)
        log = open(logdir+"log.txt","a+")
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
            subprocess.Popen(f)
        endtime = time.time()
        print("结束时间:"+time.strftime( ISOTIMEFORMAT, time.localtime(endtime)))
        print "耗时:"+str(int((endtime-starttime)/60))+"分"+str(int((endtime-starttime)%60))+"秒"
        log.close()
    else:
        print("没有找到任何APK文件,在目录:\""+ apk_dir +"\"\n请将需要反编译.apk文件放入上面的目录中.")
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
    main()


        
