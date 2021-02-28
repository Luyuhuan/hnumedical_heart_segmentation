from genericpath import exists
import os
import cv2
import json
import numpy as np
import PIL.Image
import PIL.ImageDraw
import shutil


src_path = "E:/hnumedical/Heart_segmentation/code/Choose_4CABP_SegFrame_newname/"
dst_path = "E:/hnumedical/Heart_segmentation/code/Choose_4CABP_SegFrame_newname_coco/instances_train2017.json"
img_dir = "E:/hnumedical/Heart_segmentation/code/Choose_4CABP_SegFrame_newname_coco/"
os.makedirs(img_dir)
'''
class_dict = {"背景":"__background__",
              "胸腔面积":"Chest_area",         "心脏面积":"Heart_area",
              "脊柱":"spine",         "肋骨" : "rib_cage",
              "降主动脉":"Descending_aorta",         "奇静脉":"Odd_vein",
              "肺静脉角":"Pulmonary_Vein_Angle",        "左肺":"Left_lung",
              "右心室":"Right_ventricle",           "右肺":"Right_lung",
              "右心房":"Right_atrium",      "左心房":"Left_atrium",
              "左心室":"Left_ventricle",           "三尖瓣开放":"Tricuspid_valve_opening",
              "二尖瓣开放":"Mitral_valve_opening",           "室间隔":"Ventricular_septum"}
'''
'''
class_dict = {"背景":"__background__",
              "胸腔面积":"Chest",         "心脏面积":"Heart",
              "脊柱":"spine",         "肋骨" : "rib",
              "降主动脉":"DA",         "奇静脉":"OddV",
              "肺静脉角":"PVA",        "左肺":"Llung",
              "右心室":"RV",           "右肺":"Rlung",
              "右心房":"RA",      "左心房":"LA",
              "左心室":"LV",           "三尖瓣开放":"TVO",
              "二尖瓣开放":"MVO",           "室间隔":"VS"}
'''
# class_dict = {"背景":"__background__",
#                "左心房":"LA", "右心房":"RA", "左心室":"LV", "右心室":"RV",
#               "室间隔":"VS", "房间隔":"RI", "左室壁":"LCW", "右室壁":"RCW",
#               "降主动脉":"DA", "脊柱":"SP", "肋骨":"RIB", "左肺":"Llung",
#               "右肺":"Rlung",
#               "右心室壁":"RCW", "左心室壁":"LCW"
#               }
class_dict = {"左心房":"LA", "右心房":"RA", "左心室":"LV", "右心室":"RV",
              "室间隔":"VS", "房间隔":"RI", "左室壁":"LCW", "右室壁":"RCW",
              "降主动脉":"DA", "脊柱":"SP", "肋骨":"RIB", "左肺":"Llung",
              "右肺":"Rlung"
              }
class self_format2coco(object):
    def __init__(self,json_file,save_json_path):
        '''
        :param labelme_json: 所有labelme的json文件路径组成的列表
        :param save_json_path: json保存位置
        '''

        self.json_file=json_file
        self.save_json_path=save_json_path
        self.images=[]
        self.categories=[]
        self.annotations=[]
        # self.data_coco = {}
        self.label=[]
        self.annID=0
        self.height=0
        self.width=0

        # 创建categories和label
        for lab in class_dict.values():
            self.categories.append(self.categorie(lab))
            self.label.append(lab)

        self.save_json()


    def data_transfer(self):

        # 读json
        num = 0
        for root,dirs,file in os.walk(self.json_file):
            for fil in file:
                # filename = root+'/'+dir+'/'+dir+'.json'  heng_img
                filename = root+'/'+fil
                if filename.endswith(".json"):
                    print(filename)
                    file_split = os.path.dirname(filename)
                    with open(filename,'r', encoding='UTF-8') as fp:
                        data = json.load(fp)  # 加载json文件

                        # 遍历全部图像标记
                        for img_name, info in data['annotations'].items():

                            # 当前图全部标记
                            all_anns = info['annotations']
                            # 当前图信息
                            print(img_name)
                            if len(all_anns) == 0:
                                continue
                            # print('regions=',all_anns)
                            # region_ind = 0
                            # try:
                            self.images.append(self.image(file_split+'/'+img_name+'.jpg', num))
                            # except:
                            #     print(1)
                            #     exit()

                            # 遍历当前图全部标记
                            for ann in all_anns:
                                # 解析点对
                                try:
                                    points = [[float(x.split(',')[0]), float(x.split(',')[1])] for x in ann['vertex'].split(';')]
                                    verteX = list(np.asarray(points).flatten())
                                    # 类标签
                                    label = class_dict[ann['name']]
                                    # 增加标记
                                    try:
                                        self.annotations.append(self.annotation(points, label, num))
                                    except:
                                        continue
                                    # 标记索引加1
                                    self.annID += 1
                                except:
                                    continue
                            num += 1
    def image(self,img_name,num):
        image={}
        img = None
        #height = 1080
        #width = 1920
        # *************************************** 路玉欢加的 ***************************************
        print("img_name:",img_name)
        path = img_name[:-4]
        imgrealname = path.rsplit('/',1)[1]
        #path = img_name
        # *************************************** 路玉欢加的 ***************************************
        # img = cv2.imread(path, 0)
        img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), 1)

        height, width = img.shape[:2]
        #print(img.shape)
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        # shutil.copyfile(path,img_dir+'{}'.format(str(num)+'.jpg'))
        shutil.copyfile(path, img_dir + imgrealname)

        image['height']= height
        image['width'] = width
        image['id']=num
        # image['file_name'] = str(num)+'.jpg'
        image['file_name'] = imgrealname

        self.height=height
        self.width=width

        return image

    def categorie(self,label):
        categorie={}
        categorie['supercategory'] = label
        categorie['id']=len(self.label) # 0 默认为背景
        categorie['name'] = label
        return categorie

    def annotation(self,points,label,num):
        annotation={}

        annotation['segmentation']=[list(np.asarray(points).flatten())]
        annotation['iscrowd'] = 0
        annotation['image_id'] = num
        annotation['bbox'] = list(map(float,self.getbbox(points)))

        annotation['category_id'] = self.getcatid(label)
        annotation['id'] = self.annID
        # print('annotation',annotation)
        return annotation

    def getcatid(self,label):
        for categorie in self.categories:
            #if label[1]==categorie['name']:
            if label == categorie['name']:
                return categorie['id']
        return -1

    def getbbox(self,points):
        # img = np.zeros([self.height,self.width],np.uint8)
        # cv2.polylines(img, [np.asarray(points)], True, 1, lineType=cv2.LINE_AA)  # 画边界
        # cv2.fillPoly(img, [np.asarray(points)], 1)  # 画多边形 内部像素值为1
        polygons = points
        mask = self.polygons_to_mask([self.height,self.width], polygons)
        return self.mask2box(mask)

    def mask2box(self, mask):
        '''从mask反算出其边框
        mask：[h,w]  0、1组成的图片
        1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
        '''
        # np.where(mask==1)
        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]
        # 解析左上角行列号
        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x

        # 解析右下角行列号
        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)

        return [left_top_c, left_top_r, right_bottom_c-left_top_c, right_bottom_r-left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式

    def polygons_to_mask(self,img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = PIL.Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask

    def data2coco(self):
        data_coco={}
        data_coco['images']=self.images
        data_coco['categories']=self.categories
        data_coco['annotations']=self.annotations
        return data_coco

    def save_json(self):
        self.data_transfer()
        self.data_coco = self.data2coco()
        # 保存json文件
        if not os.path.exists(os.path.dirname(self.save_json_path)):
            os.makedirs(os.path.dirname(self.save_json_path))
        json.dump(self.data_coco, open(self.save_json_path, 'w'), indent=4)  # indent=4 更加美观显示
# 转换
self_format2coco(src_path, dst_path)
