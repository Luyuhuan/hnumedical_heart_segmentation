import os
import json
import cv2
import copy
filespath = '../Choose_4CABP_SegFrame/'
AllClassList = []
def list_dir(file_dir):
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        path = file_dir + '/' + cur_file
        if os.path.isfile(path) :
            if cur_file.endswith((".json")):
                f = open(path,encoding='utf-8')
                frame = json.load(f)
                annotations = frame["annotations"]
                for i in annotations:
                    # ******************* 统计所有标注的切面名称 **********
                    if annotations[i]["bodyPart"] not in AllClassList:
                        AllClassList.append(annotations[i]["bodyPart"])
                    # **************************************************
        if os.path.isdir(path):
            list_dir(path)

list_dir(filespath)
# ****** 打印统计的切面信息******
for i in AllClassList:
    print(i)
#*************************************
