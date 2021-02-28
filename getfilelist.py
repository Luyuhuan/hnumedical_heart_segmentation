import os
import shutil

piclist = 'E:/hnumedical/Data/Video_Data/merged_video_ABP分类.txt'
piclisttxt = open(piclist,'w', encoding="utf-8")
def list_dir(file_dir):
    print(file_dir)
    piclisttxt.writelines('****************************************************************************' + '\n')
    piclisttxt.writelines(file_dir.rsplit('/',1)[1] + '\n')
    piclisttxt.writelines('****************************************************************************' + '\n')
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        path = file_dir + '/' + cur_file
        if os.path.isfile(path) :
            piclisttxt.writelines(cur_file+ '\n')
        if os.path.isdir(path):
            list_dir(path)
# list_dir("E:/hnumedical/Data/Video_Data/merged_video_视频分类")

def list_dir1(file_dir):
    print(file_dir)
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        path = file_dir + '/' + cur_file
        if os.path.isfile(path) :
            if not os.path.exists('E:/hnumedical/Data/Video_Data/merged_video_视频分类/merged_video_A4C/' +cur_file):
                if not os.path.exists('E:/hnumedical/Data/Video_Data/merged_video_视频分类/merged_video_B4C/' + cur_file):
                    shutil.copyfile(path,'E:/hnumedical/Data/Video_Data/merged_video_视频分类/merged_video_P4C/' + cur_file)
        if os.path.isdir(path):
            list_dir1(path)
list_dir1("E:/hnumedical/Data/Video_Data/merged_video")
list_dir("E:/hnumedical/Data/Video_Data/merged_video_视频分类")