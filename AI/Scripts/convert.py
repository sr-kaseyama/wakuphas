# -*- coding: utf-8 -*-
# 現状、label/stopsing_original/のtxtデータは9行まで（2桁が対応していない謎のバグ）　2018.9.10

"""
Created on Wed Dec  9 14:55:43 2015
This script is to convert the txt annotation files to appropriate format needed by YOLO 
@author: Guanghan Ning
Email: gnxr9@mail.missouri.edu
"""

import os
from os import walk, getcwd
from PIL import Image

classes = ["stopsign"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
    
    
"""-------------------------------------------------------------------""" 

""" Configure Paths"""   
mypath = "labels/stopsign_original/"
outpath = "labels/stopsign/"

cls = "stopsign"
if cls not in classes:
    exit(0)
cls_id = classes.index(cls)

wd = getcwd()
list_file = open('%s/%s_list.txt'%(wd, cls), 'w')

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    txt_name_list.extend(filenames)
    break
print(txt_name_list)

""" Process """
for txt_name in txt_name_list:
    # txt_file =  open("Labels/stop_sign/001.txt", "r")
    
    """ Open input text files """
    txt_path = mypath + txt_name
    print("\nInput:" + txt_path)
    txt_file = open(txt_path, "r")
    lines = txt_file.read().split('\n')   #for ubuntu, use "\n" instead of "\n\r"
    
    """ Open output text files """
    txt_outpath = outpath + txt_name
    print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "w")
    
    # 2桁以上のtxtは無視 modified 2018.9.16
    num_lines = sum(1 for line in open(mypath + txt_name))
    print("##### num lines", num_lines, "#####")
    if num_lines >= 10:
        continue
    
    
    """ Convert the data to YOLO format """
    ct = 0
    for line in lines:
        #print('length of line is: ')
        #print(lines, "aa")
        #print(len(line), "bb")
        #print('\n')
        if(len(line) >= 2):
            #if((len(line) >= 2) and (li < 10)):
            ct = ct + 1
            #print(line + "cc")
            elems = line.split(' ')
            #print(elems)
            xmin = elems[0]
            xmax = elems[2]
            ymin = elems[1]
            ymax = elems[3]
            #
            img_path = str('%s/images/%s/%s.jpg'%(wd, cls, os.path.splitext(txt_name)[0]))
            #t = magic.from_file(img_path)
            #wh= re.search('(\d+) x (\d+)', t).groups()
            im=Image.open(img_path)
            w= int(im.size[0])
            h= int(im.size[1])
            #w = int(xmax) - int(xmin)
            #h = int(ymax) - int(ymin)
            # print(xmin)
            #print(w, h)
            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert((w,h), b)
            print(bb)
            txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    """ Save those images with bb into list"""
    if(ct != 0):
        list_file.write('%s/images/%s/%s.jpg\n'%(wd, cls, os.path.splitext(txt_name)[0]))
                
list_file.close()       
