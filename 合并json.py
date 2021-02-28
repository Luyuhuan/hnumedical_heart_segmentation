import os
import codecs 
import cv2
import json
stdpath = "C:/Users/wh/Desktop/A4Cothers_stdjson"
cyclepath = "C:/Users/wh/Desktop/A4Cothers_cycle"
newjsonpath = "C:/Users/wh/Desktop/newjson"
def list_cycle_dir(file_dir):
    file_list = os.listdir(file_dir)
    for file in file_list:
        if file.endswith(".json"):
            stdjsonpath = os.path.join(stdpath, file.rsplit("-",1)[0]+".json")
            stdjson = open(stdjsonpath,encoding='utf-8')
            # print("stdjson:",stdjson)
            stdframe = json.load(stdjson)
            annotationsstd = stdframe["annotations"]
            fcycle = open(os.path.join(file_dir, file), encoding='utf-8')
            framecycle = json.load(fcycle)
            annotationscycle = framecycle["annotations"]
            for frame in annotationscycle:
                cyclereal = annotationscycle[frame]["info"]
                # print("frame:",frame)
                # print("cyclereal:",cyclereal)
                # print("annotationsstd[frame][annotations]:",annotationsstd[frame]["info"])
                annotationsstd[frame]["info"] = cyclereal
            newjson = os.path.join(newjsonpath,file.rsplit("-",1)[0]+".json")
            with open(newjson, "w", encoding='utf-8') as f1:
                json.dump(stdframe, f1, ensure_ascii=False, sort_keys=True, indent=4)
            f1.close()

list_cycle_dir(cyclepath)