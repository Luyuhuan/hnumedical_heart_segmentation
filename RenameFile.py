import os
import shutil
# 合并所有的视频到同一文件夹并重命名
# 合并的目标路径
GetAll_path = "D:/BaiduNetdiskDownload/孕周分类视频合并中晚孕期视频"
if not os.path.exists(GetAll_path):
    os.makedirs(GetAll_path)
def GetAll(file_dir):
    dir_list = os.listdir(file_dir)
    print("处理到 %s 文件夹" % file_dir)
    for cur_file in dir_list:
        path = file_dir + '/' + cur_file
        if os.path.isfile(path) :
            week = (file_dir.split('/')[-2])[:2]
            if week == "未知":
                week = "X"
            newname = week+'week_'+cur_file
            if os.path.exists(os.path.join(GetAll_path, newname)):
                print(os.path.join(GetAll_path, cur_file),"视频命名重复了！！！！！！！！！！！！！！！！！！！！！！！！！！！")
                continue
            shutil.copyfile(path,os.path.join(GetAll_path, newname))
        if os.path.isdir(path):
            GetAll(path)
GetAll("D:/BaiduNetdiskDownload/孕周分类视频")
#GetAll("D:/BaiduNetdiskDownload/中晚孕期视频")