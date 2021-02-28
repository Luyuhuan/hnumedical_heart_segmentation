import os
import codecs 
import cv2
import numpy as np
# 指定最终视频的切面类型
Type_4C = "A4C"
# 指定原始视频文件夹路径、存储中间帧图片路径（如果不存在 自动创建）、存储最终视频路径（如果不存在 自动创建）
orgvideopath = "C:/Users/wh/Desktop/org_video"
framespath = "C:/Users/wh/Desktop/frames"
savevideopath = "C:/Users/wh/Desktop/savevideo"
if not os.path.exists(framespath):
    os.makedirs(framespath)
if not os.path.exists(savevideopath):
    os.makedirs(savevideopath)
# 先将原始视频处理成帧图片
def list_video_dir(file_dir):
    video_list = os.listdir(file_dir)
    for video in video_list:
        print("处理 %s 视频中......" % video)
        # 创建视频对应的帧图片文件夹
        imagespath = os.path.join(framespath,video[:-4])
        if not os.path.exists(imagespath):
            os.makedirs(imagespath)
        # 将视频处理成帧图片
        cap = cv2.VideoCapture(os.path.join(file_dir,video))
        framecount = 0
        while (1):
            success, frame = cap.read()
            if success:
                cv2.imencode('.jpg', frame)[1].tofile(os.path.join(imagespath ,video[:-4] + "_%05d" % framecount + '.jpg'))
                framecount = framecount + 1
            else:
                break
        cap.release()

list_video_dir(orgvideopath)
'''
上面函数执行完毕之后 
人工挑选目标切面保留（连续帧） 其他帧图片删除
执行下面的函数合成新视频
'''
def list_frame_dir(file_dir):
    dir_list = os.listdir(file_dir)
    for dir in dir_list:
        print("处理 %s 视频中......" % dir)
        # 获取原视频的高、宽、fps信息
        if os.path.exists(os.path.join(orgvideopath, dir+".avi")):
            orgvideo_cap = cv2.VideoCapture(os.path.join(orgvideopath, dir+".avi"))
        elif os.path.exists(os.path.join(orgvideopath, dir+".AVI")):
            orgvideo_cap = cv2.VideoCapture(os.path.join(orgvideopath, dir+".AVI"))
        frame_width = int(orgvideo_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(orgvideo_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = orgvideo_cap.get(cv2.CAP_PROP_FPS)
        # 对当前留下的帧进行合成
        video_path = os.path.join(savevideopath, dir+"_"+Type_4C+".avi")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(video_path, fourcc, fps, (frame_width, frame_height))
        frame_list = os.listdir(os.path.join(file_dir,dir))
        for frame in frame_list:
            img = cv2.imdecode(np.fromfile(os.path.join(file_dir,dir,frame), dtype=np.uint8), 1)
            writer.write(img)
# list_frame_dir(framespath)