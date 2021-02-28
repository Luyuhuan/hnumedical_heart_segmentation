import csv
import  shutil
#coding=utf-8
import re
import codecs
import os
import json
import cv2
import numpy as np
#os.environ['CUDA_VISIBLE_DEVICES'] = '0,5'
atr1 = {'丘脑水平横切面':'QiuNaoShuiPinHeng','侧脑室水平横切面':'CeNaoShiShuiPinHeng','小脑水平横切面':'XiaoNaoShuiPinHeng',
'双眼球横切面':'ShuangYanQiuHeng','颜面部正中状切面':'YanMianBuZhengZhongZhuang','鼻唇冠状切面':'BiChunGuanZhuang',
'外耳廓矢状切面':'WaiErKuoShiZhuang','颅顶部横切面':'LuDingBuHeng','透明隔腔水平横切面':'TouMingGeQiangShuiPinHeng',
'胎儿颅脑正中矢状切面':'TaiErLuNaoZhengZhongShiZhuang','旁中央矢状切面':'PangZhongYangShiZhuang','大脑半球矢状切面':'DaNaoBanQiuShiZhuang',
'小脑冠状切面':'XiaoNaoGuanZhuang','侧脑室三角区冠状切面':'CeNaoShiSanJiaoQuGuanZhuang','枕叶冠状切面':'ZhenYeGuanZhuang',
'经额叶冠状切面':'JinEYeGuanZhuang','经前角冠状切面':'JinQianJiaoGuanZhuang','经侧脑室体部冠状切面':'JinCeNaoShiTiBuGuanZhuang'
}
atr2 = {'心尖四腔心切面':'XinJianSiQiangXin','胸骨旁四腔心切面':'XiongGuPangSiQiangXin','心底四腔心切面':'XinDiSiQiangXin',
'心尖五腔心':'XinJianWuQiangXin','左室流出道切面':'ZuoShiLiuChuDao','右室流出道切面':'YouShiLiuChuDao',
'心底短轴切面':'XinDiDuanZhou','3VV切面':'3VV','3VT切面':'3VT',
'左侧胸腔矢状切面':'ZuoCeXiongQiangShiZhuang','右侧胸腔矢状切面':'YouCeXiongQiangShiZhuang','胸腔冠状切面':'XiongQiangGuanZhuang'
}
atr3 = {'胆囊水平横切面':'DanNangShuiPingHeng','脐孔水平腹部横切面':'QiKongShuiPinFuBuHeng','双肾横切面':'ShuangShenHeng',
'左肾矢状切面':'ZuoShenShiZhuang','右肾矢状切面':'YouShenShiZhuang','双肾冠状切面':'ShuangShenGuanZhuang',
'上腹部横切面':'ShangFuBuHeng','膀胱水平横切面彩色多普勒':'PangGuangShuiPinHengCaiSeDuoPuLe'
}
atr4 = {'颈胸段脊柱矢状切面':'JinXiongDuanJiZhuShiZhuang','腰骶尾段脊柱矢状切面':'YaoDiWeiDuanJiZhuShiZhuang','胎儿肩胛骨横切面':'TaiErJianJiaGuHeng',
'肱骨纵切面':'HongGuZong','胎儿前臂冠状切面':'TaiErQianBiGuanZhuang','手掌冠状切面':'ShouZhangGuanZhuang',
'手掌横切面':'ShouZhangHeng','胎儿双侧髂骨横切面':'TaiErShuangCeKeGuHeng','股骨纵切面':'GuGuzong',
'胫腓骨冠状切面':'JingFeiGuGuanZhuang','足底切面':'ZuDi','腿矢状切面':'TuiShiZhuang',
'前臂冠状切面':'QianBiGuanZhuang','胸腰段脊柱矢状切面':'XiongYaoDuanJiZhuShiZhuang'
}
atr5 = {'胎盘脐带插入口':'TaiPanQiDaiChaRuKou','宫颈内口矢状切面':'GongJingNeiKouShiZhuang'
}
atr_A4c_B4C_P4C={'心尖四腔心切面':'XinJianSiQiangXin','胸骨旁四腔心切面':'XiongGuPangSiQiangXin','心底四腔心切面':'XinDiSiQiangXin'}

sequences = {'左心室': 0, '右心室': 1, '左心房': 2, '右心房': 3, '左室壁':4,'右室壁':5,'室间隔':6,'房间隔':7,'二尖瓣开放': 8, '三尖瓣开放': 9, '二尖瓣关闭': 10, '三尖瓣关闭': 11,'卵圆孔瓣':12,'肺静脉角':13,'左肺': 14, '右肺': 15, '脊柱': 16,
             '肋骨': 17, '降主动脉': 18,'奇静脉':19}

# 新增颅骨数据时使用
# clsnames = ['胼胝体', '透明隔', '丘脑', '第三脑室', '大脑镰', '侧脑室前角', '大脑实质', '侧脑室后角', '脉络丛', '颅骨光环', '脑岛', '大脑外侧裂', '穹窿柱',
#             '透明隔腔',
#             '颞上沟', '颞下沟', '顶枕沟', '额上沟', '扣带沟', '额下沟']  # # 背景部分的类标设置为0
# exceptions = ['Polygon']

# 针对： 丘脑水平横切面，侧脑室水平横切面，小脑水平横切面
clsnames = ['左心室', '右心室', '左心房', '右心房', '左室壁','右室壁','室间隔','房间隔','二尖瓣开放', '三尖瓣开放', '二尖瓣关闭', '三尖瓣关闭','卵圆孔瓣','肺静脉角','左肺', '右肺', '脊柱',
             '肋骨', '降主动脉','奇静脉',]

#sequences = {'左心室': 0}
#clsnames = ['左心室']

# 新增颅骨数据时使用
# clsnames = ['胼胝体', '透明隔', '丘脑', '第三脑室', '大脑镰', '侧脑室前角', '大脑实质', '侧脑室后角', '脉络丛', '颅骨光环', '脑岛', '大脑外侧裂', '穹窿柱',
#             '透明隔腔',
#             '颞上沟', '颞下沟', '顶枕沟', '额上沟', '扣带沟', '额下沟']  # # 背景部分的类标设置为0
# exceptions = ['Polygon']

# 针对： 丘脑水平横切面，侧脑室水平横切面，小脑水平横切面

exceptions = ['Polygon']

#annos_dir_train="G:\\心脏分割\\renew_images_segemation_label_216"
#images_dir_train='G:\\心脏分割\\renew_images_segemation_216'
countall ={}
count = 0
picchoose = 0
def mkdir(path):
    path=path.strip()
    path=path.rstrip("/")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print (path+' 创建成功')
        return True
    else:
      #print (path+' 目录已存在')
      return False
def list_dir(file_dir):
  dir_list = os.listdir(file_dir)
  for cur_file in dir_list:
    # 获取文件的绝对路径
    path = file_dir+'/'+cur_file
    print("cur_file",cur_file)
    #print(path)
    if os.path.isfile(path) and os.path.exists(path[:-4]+'.json'): # 判断是否是文件还是目录需要用绝对路径
      #print( "{0} : is file!".format(cur_file))
      f = open(path[:-4] + '.json', encoding='utf-8')
      jsonframe = json.load(f)
      # print(path[:-4]+'.json')
      print(path[:-4] + '.json')
      annotations = jsonframe["annotations"]
      cap = cv2.VideoCapture(path)
      #print("成功")
      framecount=0
      judge_suzhang_shousuo=0
      while(1):
        success, frame = cap.read()
        if success:
          #cv2.imwrite(images+cur_file[:-4] +"_%03d" % framecount + '.jpg',frame)
          #print(path[:-4]+'.json')
          #print(jsonframe["annotations"])
          #print(framecount)

          if str(framecount) in annotations and annotations[str(framecount)]['bodyPart'] in atr_A4c_B4C_P4C:

              #annos_dir_train ="C:\\Users\\pb\Desktop\\test_chinese"
              #images_dir_train ='C:\\Users\\pb\\Desktop\\test_chinese1'
              annos_dir_train = "E:/hnumedical/Heart_segmentation/Choose_A4C_SegFrame_label"
              images_dir_train = 'E:/hnumedical/Heart_segmentation/Choose_A4C_SegFrame_image'
              mkdir(annos_dir_train)
              mkdir(images_dir_train)

              annotations_type=annotations[str(framecount)]['annotations']
              #print("annotations_type",annotations_type)
              #print(type(annotations_type))
              #shutil.copy(path, path_target)
              #shutil.copy(path[:-4] + ".json", path_target)
              if str(annotations_type).find("[]")<0:
                  merge_set = []
                  clsname_only = True
                  print("framecount", framecount)
                  print("annotations_type",annotations_type)

                  src_image = frame
                  print("src_image", src_image.shape)
                  anno_image = np.zeros_like(src_image)
                  # TODO 由于各组织之间可能存在覆盖重叠关系，所以在画标注图时要注意画的次序
                  regions = [region for region in annotations_type if
                             'name' in region.keys() and 'vertex' in region.keys()]
                  print("regions",regions)
                  regions = sorted(regions, key=lambda region: sequences[region['name']] if region[
                                                                                                'name'] in sequences.keys() else len(
                      sequences))
                  #print("regions", regions)
                  # print([region['name'] for region in regions])
                  for region in regions:
                      print("region",region)
                      try:
                          clsname, vertex = region['name'], region['vertex']
                          print("clsname",clsname)
                          print("vertex", vertex)
                          print("jinlai")
                      except:
                          print(region)
                          continue
                      if clsname.strip() == '':
                          continue
                      if exceptions and clsname in exceptions:
                          continue
                      if merge_set and clsname in merge_set:
                          clsname = 'merged'
                      if clsname in clsnames:
                          cls_value = clsnames.index(clsname) + 1

                          print("clsnames.index(clsname)",clsnames.index(clsname))
                      else:
                          if clsname_only:
                              continue
                          clsnames.append(clsname)
                          cls_value = len(clsnames)

                      points = [
                          [[int(float(p.split(',')[0])), int(float(p.split(',')[1]))] for p in
                           vertex.strip().split(';')]]
                      print("points", points)
                      print("cls_value==============================",cls_value)
                      cv2.fillPoly(anno_image, np.array(points, dtype=np.int32), (cls_value,cls_value,cls_value))
                      #cv2.imshow('image',anno_image)
                      #cv2.waitKey(0)

                      # cv2.imshow('anno', anno_image)
                      # cv2.waitKey(0)
                  new_name = cur_file[:-4]+"_"+str(framecount)
                  print("new_name",new_name)
                  print("anno_image",anno_image.shape)
                  print("type(src_image)",type(src_image))
                  print("type(anno_image)", type(anno_image))
                  print("a",os.path.join(images_dir_train, '{}.png'.format(new_name)))
                  cv2.imencode('.jpg', frame)[1].tofile(os.path.join(images_dir_train, '{}.jpg'.format(new_name)))
                  ###cv2.imwrite(os.path.join(images_dir_train, '{}.png'.format(new_name)), src_image)
                  #cv2.imencode('.jpg', frame)[1].tofile(picfile + cur_file[:-4] + "_%03d" % framecount + '.jpg')
                  ###cv2.imwrite(os.path.join(annos_dir_train, '{}.png'.format(new_name)), anno_image)
                  cv2.imencode('.jpg', anno_image)[1].tofile(os.path.join(annos_dir_train, '{}.jpg'.format(new_name)))
                  judge_suzhang_shousuo+=1
                  #if judge_suzhang_shousuo == 2:
                      #break

          framecount=framecount+1
        else:
          break
      cap.release()
    if os.path.isdir(path):
      #print( "{0} : is dir!".format(cur_file))
      list_dir(path) # 递归子目录
  #f.close()

#images = 'E:/hnuultrasonic/newDetection/framepic分类Real/'
#f = open('腹部标注.csv','w',newline="")
#csv_writer = csv.writer(f)
list_dir("../video_data/标注汇总")
print(count)
#f.close()
