import os
import codecs 
import cv2
import json
import copy

namemap = {"舒张末期":"Dd","收缩末期":"Ds"}
imagespath = 'C:/Users/wh/Desktop/new_A4C_1111_res_DsDd/'
videopath = "C:/Users/wh/Desktop/new_A4C_1111"
jsonpath = "C:/Users/wh/Desktop/new_A4C_1111_res"
videofiles = os.listdir(videopath)
jsonfiles = os.listdir(jsonpath)
videocount = 0
config_new = {
"annotations" : {}
}
save_json = copy.deepcopy(config_new)
for file in jsonfiles:
    Count = {"Dd":0,"Ds":0}
    if file.endswith("json"):
        print("file:",file)
        f = open(os.path.join(jsonpath, file), encoding='utf-8')
        frame = json.load(f)
        annotations = frame["annotations"]
        videoname = file[:-12]
        if os.path.exists(os.path.join(videopath, videoname+".avi")):
            cap = cv2.VideoCapture(os.path.join(videopath, videoname+".avi"))
        elif os.path.exists(os.path.join(videopath, videoname+".AVI")):
            cap = cv2.VideoCapture(os.path.join(videopath, videoname+".AVI"))
        framecount=0
        while(1):
            success, frame = cap.read()
            if success:
                if str(framecount) in annotations:
                    info = namemap[annotations[str(framecount)]["info"]]
                    if Count[info] <2:
                        picname = videoname + "_%05d_" % framecount + info+'.jpg'
                        cv2.imencode('.jpg', frame)[1].tofile(os.path.join(imagespath+ picname))
                        save_json['annotations'][picname] = annotations[str(framecount)]
                        Count[info] = Count[info] + 1
                framecount=framecount+1
            else:
                break
        cap.release()
    videocount = videocount + 1
new = os.path.join(imagespath, 'annotations.json')
with open(new, "w", encoding='utf-8') as f:
    json.dump(save_json, f, ensure_ascii=False, sort_keys=True, indent=4)
f.close()
print("videocount:",videocount)