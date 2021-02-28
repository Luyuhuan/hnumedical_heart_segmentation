# -*- encoding: utf-8 -*-
import cv2
import os
import json
import copy
config_new={'annotations':{}}
picdir = 'E:/hnumedical/Heart_segmentation/DsDdPic/'
save_json = {}
save_json = copy.deepcopy(config_new)
def makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
def list_dir(file_dir):
  dir_list = os.listdir(file_dir)
  count =0
  for cur_file in dir_list:
    # 获取文件的绝对路径
    count = count + 1
    print('count:',count)
    path = file_dir+'/'+cur_file
    if os.path.isfile(path):
        if cur_file[-4:] == '.wmv' or cur_file[-4:] == '.AVI' or cur_file[-4:] == '.mp4' or cur_file[-4:] == '.avi':
            f = open(path[:-4]+'.json',encoding='utf-8')
            frame = json.load(f)
            annotations = frame["annotations"]
            ShuZhangList = []
            ShouSuoList = []
            for i in annotations:
                if annotations[i]["info"] == "舒张末期":
                    ShuZhangList.append(i)
                elif annotations[i]["info"] == "收缩末期":
                    ShouSuoList.append(i)
            ShuZhangChoose = ShuZhangList[int(len(ShuZhangList)/2)]
            ShouSuoChoose = ShouSuoList[int(len(ShouSuoList)/2)]
            cap = cv2.VideoCapture(path)
            framecount=0
            while(1):
                success, frame = cap.read()
                if success and str(framecount) in annotations:
                    if str(framecount) == ShuZhangChoose or str(framecount) == ShouSuoChoose:
                        cv2.imencode('.jpg', frame)[1].tofile(picdir + cur_file[:-4] + "_%05d" % framecount + '.jpg')
                        save_json['annotations'][cur_file[:-4] + "_%05d" % framecount + '.jpg'] = annotations[str(framecount)]
                    framecount=framecount+1
                else:
                    break
            cap.release()
    if os.path.isdir(path):
        list_dir(path) # 递归子目录
list_dir('E:/hnumedical/Data/Video_Data/merged_video')

new = picdir+'annotations.json'
with open(new, "w", encoding='utf-8') as f:
    json.dump(save_json, f, ensure_ascii=False, sort_keys=True, indent=4)
f.close()