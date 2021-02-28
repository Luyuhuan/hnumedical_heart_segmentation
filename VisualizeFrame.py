import os
import json
import cv2
import numpy as np
import random

atr_A4c_B4C_P4C={"心尖四腔心切面":"A4C","心底四腔心切面":"B4C","胸骨旁四腔心切面":"P4C"}

sequences = {'左心室': 0, '右心室': 1, '左心房': 2, '右心房': 3,
             '左室壁':4,'右室壁':5,'室间隔':6,'房间隔':7,
             '左肺': 8, '右肺': 9,'脊柱': 10,'肋骨': 11,
             '降主动脉': 12,
             '左心室壁':4, '右心室壁':5}
clsnames = ['左心室', '右心室', '左心房', '右心房',
             '左室壁','右室壁','室间隔','房间隔',
             '左肺', '右肺','脊柱','肋骨',
             '降主动脉',
             '左心室壁', '右心室壁']
exceptions = ['Polygon']
black_save_dir = 'E:/hnumedical/Heart_segmentation/Choose_4CABP_SegFrame_black'
res_save_dir = 'E:/hnumedical/Heart_segmentation/Choose_4CABP_SegFrame_res'
os.makedirs(black_save_dir)
os.makedirs(res_save_dir)

def list_dir(file_dir):
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        path = file_dir+'/'+cur_file
        if os.path.isfile(path) and cur_file == "annotations.json":
            f = open(path, encoding='utf-8')
            jsonframe = json.load(f)
            annotations = jsonframe["annotations"]
            for img in annotations:
                imgpath = file_dir + '/' + img
                image = cv2.imdecode(np.fromfile(imgpath, dtype=np.uint8), 1)
                if annotations[img]['bodyPart'] in atr_A4c_B4C_P4C:
                    annotations_type=annotations[img]['annotations']
                    if str(annotations_type).find("[]")<0:
                        merge_set = []
                        clsname_only = True
                        print("annotations_type",annotations_type)
                        src_image = image
                        print("src_image", src_image.shape)
                        anno_image = np.zeros_like(src_image)
                        # TODO 由于各组织之间可能存在覆盖重叠关系，所以在画标注图时要注意画的次序
                        regions = [region for region in annotations_type if
                                   'name' in region.keys() and 'vertex' in region.keys()]
                        print("regions",regions)
                        regions = sorted(regions, key=lambda region: sequences[region['name']] if region['name'] in sequences.keys() else len(sequences))
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
                        new_name = img
                        print("new_name",new_name)
                        print("anno_image",anno_image.shape)
                        print("type(src_image)",type(src_image))
                        print("type(anno_image)", type(anno_image))
                        #cv2.imwrite(os.path.join(black_save_dir, '{}.png'.format(new_name)), anno_image)
                        cv2.imencode('.png', anno_image)[1].tofile(os.path.join(black_save_dir, '{}.png'.format(new_name[:-4])))
        if os.path.isdir(path):
            list_dir(path) # 递归子目录

random.seed(1)
class_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(5000)]

def visualize_anno(seg_img_path, n_classes=50, save_dir=None, show=False, colors=class_colors):
    """@WareLee
    将标注信息可视化

    :param seg_img_path: 分割结果图片地址
    :param n_classes: 被分割区域的类别数量
    :param save_dir: 可视化效果图的保存位置,为None时不保存
    :param show: 是否在线展示
    :return: None
    """
    assert os.path.exists(seg_img_path), 'Error : {} is not exists ... '.format(seg_img_path)
    if save_dir and not os.path.exists(save_dir):
        os.makedirs(save_dir)
    #seg = cv2.imread(seg_img_path)
    seg = cv2.imdecode(np.fromfile(seg_img_path, dtype=np.uint8), 1)
    seg_img = np.zeros_like(seg)
    for c in range(n_classes):
        seg_img[:, :, 0] += ((seg[:, :, 0] == c) * (colors[c][0])).astype('uint8')
        seg_img[:, :, 1] += ((seg[:, :, 0] == c) * (colors[c][1])).astype('uint8')
        seg_img[:, :, 2] += ((seg[:, :, 0] == c) * (colors[c][2])).astype('uint8')
    if save_dir:
        #cv2.imwrite(os.path.join(save_dir, os.path.basename(seg_img_path)), seg_img)
        cv2.imencode('.png', seg_img)[1].tofile(os.path.join(save_dir, os.path.basename(seg_img_path)))
    if show:
        cv2.imshow(os.path.basename(seg_img_path), seg_img)
        cv2.waitKey(0)


def _vialize_all_anno(n_classes=50,black_dir='',save_dir=''):
    for seg_name in os.listdir(black_dir):
        if seg_name.endswith(('.png', '.jpg', '.jpeg')):
            visualize_anno(os.path.join(black_dir, seg_name), save_dir=save_dir, n_classes=n_classes, colors=class_colors)

list_dir("E:/hnumedical/Heart_segmentation/Choose_4CABP_SegFrame")
_vialize_all_anno(13,black_save_dir,res_save_dir)