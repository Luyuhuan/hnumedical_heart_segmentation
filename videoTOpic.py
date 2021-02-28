import os
import codecs 
import cv2
imagespath = 'C:/Users/wh/Desktop/1frame/'
videopath = "C:/Users/wh/Desktop/1/" #文件夹目录
files= os.listdir(videopath) #得到文件夹下的所有文件名称
videocount =0
for file in files: 
    cap = cv2.VideoCapture(videopath+file)
    framecount=0
    while(1):
        success, frame = cap.read()
        if success:
            #cv2.imwrite(images+ file[:-4] +"_%03d" % framecount + '.jpg',frame)
            cv2.imencode('.jpg', frame)[1].tofile(imagespath+ file[:-4] +"_%05d" % framecount + '.jpg')
            framecount=framecount+1
        else:
            break
    cap.release()
    videocount = videocount + 1