import os
import json
import cv2
import copy
imagespath = '../Choose_4CABP_SegFrame_newname/'
videopath = '../../All_video_data'
os.makedirs(imagespath)
config_new = {
    "annotations":{}
}
AllClassList = []
AllSegList = {}
ClassChoose = {"心尖四腔心切面":0,"心底四腔心切面":0,"胸骨旁四腔心切面":0}
ChooseSeg = ["左心房","右心房","左心室","右心室",
             "室间隔","房间隔","左室壁","右室壁",
             "降主动脉","脊柱","肋骨","左肺",
             "右肺"]
ChangeName = {"右心室壁":"右室壁","左心室壁":"左室壁"}
save_json = copy.deepcopy(config_new)
def list_dir(file_dir):
    dir_list = os.listdir(file_dir)
    NowCount = 1
    for cur_file in dir_list:
        path = file_dir + '/' + cur_file
        if os.path.isfile(path) :
            if cur_file.endswith(("AVI","WMV","avi","wmv","MP4")):
                print("处理第 %05d 个视频！" % (NowCount) )
                NowCount = NowCount + 1
                pathjson = path[:-4] + '.json'
                f = open(pathjson,encoding='utf-8')
                frame = json.load(f)
                annotations = frame["annotations"]
                # **********************************选择心尖,心底,胸骨旁标注数据**************************************************
                ChooseFrame = []
                for i in annotations:
                    # ******************* 统计所有标注的切面名称 **********
                    if annotations[i]["bodyPart"] not in AllClassList:
                        AllClassList.append(annotations[i]["bodyPart"])
                    # **************************************************
                    if (annotations[i]["bodyPart"] in ClassChoose ) and (len(annotations[i]["annotations"]) >=5) :
                        ClassChoose[annotations[i]["bodyPart"]] = ClassChoose[annotations[i]["bodyPart"]] + 1
                        ChooseFrame.append(i)
                        # ******************* 统计三个四腔心切面所有的标注结构 **************
                        if annotations[i]["bodyPart"] not in AllSegList:
                            AllSegList[annotations[i]["bodyPart"]] = []
                        for j in annotations[i]["annotations"]:
                            if j["name"] not in AllSegList[annotations[i]["bodyPart"]]:
                                AllSegList[annotations[i]["bodyPart"]].append(j["name"])
                        # ***************************************************************
                # **************************************************************************************************

                # ***********************************存下图片,存下json************************************************
                print(path)
                capture = cv2.VideoCapture(path)
                if not capture.isOpened():
                    raise ValueError('Failed to open video: ' + path)
                ret, image = capture.read()
                print("ChooseFrame:",ChooseFrame)
                framecount = 0
                while ret:
                    if str(framecount) in ChooseFrame :
                        imgname = cur_file[:-4] + "_%05d" % (framecount) + '.jpg'
                        cv2.imencode('.jpg', image)[1].tofile(imagespath + imgname)
                        # **************** 选择训练的结构 保存json ***************
                        global save_json
                        save_json["annotations"][imgname] = copy.deepcopy(annotations[str(framecount)])
                        save_json["annotations"][imgname]["annotations"] = []
                        CountStr = {"左心房":0,"右心房":0,"左心室":0,"右心室":0,
                                    "室间隔":0,"房间隔":0,"左室壁":0,"右室壁":0,
                                    "降主动脉":0,"脊柱":0,"肋骨":0,"左肺":0,
                                    "右肺":0}
                        for ano in annotations[str(framecount)]["annotations"]:
                            if ano["name"] in ChooseSeg:
                                save_json["annotations"][imgname]["annotations"].append(ano)
                                CountStr[ano["name"]] = CountStr[ano["name"]] + 1
                            elif ano["name"] in ChangeName:
                                nowano = copy.deepcopy(ano)
                                nowano["name"] = ChangeName[ano["name"]]
                                nowano["alias"] = ChangeName[ano["name"]]
                                save_json["annotations"][imgname]["annotations"].append(nowano)
                                CountStr[nowano["name"]] = CountStr[nowano["name"]] + 1
                        print(cur_file,str(framecount),"多了以下结构：")
                        for i in CountStr:
                            if CountStr[i] > 1 and i != "肋骨":
                                print(i,":",CountStr[i])
                            elif CountStr[i] > 2 and i == "肋骨":
                                print(i,":",CountStr[i])
                        #*******************************************************
                    ret, image = capture.read()
                    framecount = framecount + 1
                # **************************************************************************************************

        if os.path.isdir(path):
            list_dir(path)

list_dir(videopath)

# ************************* 写入json文件 ************************************
new1 = imagespath+'annotations.json'
with open(new1, "w", encoding='utf-8') as f1:
    json.dump(save_json, f1, ensure_ascii=False, sort_keys=True, indent=4)
f1.close()
# **************************************************************************
# ****** 打印统计的切面信息 结构信息 ******
print("AllClassList:",AllClassList)
for i in AllClassList:
    print(i)
for i in AllSegList:
    print(i)
    print(AllSegList[i])
for i in ClassChoose:
    print(i,":",ClassChoose[i])
#*************************************
