# -*- coding: GBK -*-

import os
import shutil   
import re     
import zipfile
import time
import shutil

ISOTIMEFORMAT="%Y-%m-%d %X"
apktool_bat="lib\\apktool1.5.1\\apktool.bat"
dex2jar_bat="lib\\dex2jar-0.0.9.13\\d2j-dex2jar.bat"
jd_gui_exe="lib\\jd-gui-0.3.5\\jd-gui.exe"
apk_dir="apk"


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
    text =  execCmd(jd_gui_exe + " "+"\""+distApkDir+ os.sep +"classes.jar"+"\"")
    for f in text:
        print f
		
def main():
    starttime =  time.strftime( ISOTIMEFORMAT, time.localtime() )
    print("开始时间:"+starttime+"\n")
    currentDir =  os.getcwd()
    apks = getAPK()
    if len(apks)>0 :        
##       print("上级目录:"+os.path.abspath(os.pardir )+"\n")
        print("当前目录:"+currentDir+"\n")
        distdir = os.path.abspath(currentDir)+ os.sep  +"dist"
        print("结果目录:"+distdir+"\n")
        if os.path.exists(distdir):
            shutil.rmtree(distdir)
        os.makedirs(distdir)
        logdir = os.path.abspath(currentDir)+ os.sep  +"dist_log"
        print("日志目录:"+logdir+"\n")
        if os.path.exists(logdir):
            shutil.rmtree(logdir)
        os.makedirs(logdir)
        i = 0
        length =  len(apks)
        for f in apks:
            i = i +1
            print str(i)+"/"+str(length)
            decompileApk(distdir,f,logdir)
        print("结束时间:"+time.strftime( ISOTIMEFORMAT, time.localtime())+"\n")
    else :
        print("没有找到任何APK文件在目录:"+os.path.abspath(currentDir)+ os.sep  + apk_dir +"\n")
    raw_input("Press any key to exit")
main()
        
