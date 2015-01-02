# -*- coding: utf-8 -*-
# FileName: batchrename.py
# Function: 
'''
    批量命名某一文件夹下的文件名
    (1) 把当前文件夹的所用文件命名为当前文件夹名+"_"+原来的文件名
    (2) 即文件夹Data,里面有1.png,2.png,运行里面的xx.py就变成了Data_1.png,Data_2.png
    (3) 还有一个条件就是当文件名已经是 文件夹名_ 就不用再重命名了，即Data_1.png 再执行脚本就不会变成Data_Data_1.png
    (4) 过滤[".py", ".exe"], 这些文件不重命名
'''

import sys
import os
import os.path
import re

FilterList = [".py", ".exe"];

def getParentPath(strPath):
    if not strPath:
        return None;
    parentPath = os.path.basename(strPath); #父目录名
    print(parentPath);
    return parentPath;  
   
def BatchRename(dirPath):
    print("当前的路径是: %s" % dirPath);
    strPath = dirPath.split('\\')[-1];
    print(strPath);

    parentPath = getParentPath(strPath);    #父目录名
    #设置路径
    os.chdir(dirPath);
    #os.chdir(sys.argv);
    print(sys.argv);
    fileList = os.listdir(os.curdir);
    for obj in fileList:
        (fileName, fileExt) = os.path.splitext(obj);
        print(fileName, fileExt);

        #过滤
        if fileExt in FilterList:   
            continue;

        #如果文件名包含 "父目录名_"，则跳过; 即如demo_121.txt 父目录是demo, 跳过
        #match ：只从字符串的开始与正则表达式匹配，匹配成功返回matchobject，否则返回None, None即false
        #pattern：parentPath + "_"
        m = re.match(parentPath + "_", fileName);
        if m:
            continue;

        #如果对象是目录， 则递归下去
        if (os.path.isdir(os.curdir + "/" + obj)):
            print(os.curdir);
            BatchRename(os.curdir + "/" + obj);
            os.chdir(os.pardir);
        else:            
            fileFullName = parentPath + "_" + fileName + fileExt;
            os.rename(obj, fileFullName);
            print(fileFullName);

def main():
    #获取脚本路径
    dirPath = cur_file_dir();
    BatchRename(dirPath);

    #confirm = raw_input('Confirm(y|n): ');
    #if confirm == ('y' or 'Y'):
        #获取脚本路径
        #dirPath = cur_file_dir();
        #BatchRename(dirPath);
    #else:
        #sys.exit();



#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

if __name__ == '__main__':
    main();