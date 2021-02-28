import glob
import os

import numpy as np
import cv2
import random
import argparse
import shutil



random.seed(1)
class_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(5000)]


def visualize_single_seg(seg, n_classes, ignore_cls=0):
    """可视化单个分割标记图"""
    if isinstance(seg, str):
        seg = cv2.imread(seg)
    assert len(seg.shape) == 2 or len(seg.shape) == 3, 'Dimention of seg must be 2 or 3, not {}'.format(
        len(seg.shape, ))

    if len(seg.shape) == 3:
        seg = seg[:, :, 0]
    colors = class_colors
    seg_img = np.zeros((*(seg.shape), 3), np.uint8)

    for c in range(n_classes):
        if ignore_cls is None or c != ignore_cls:
            seg_img[:, :, 0] += ((seg[:, :] == c) * (colors[c][0])).astype('uint8')
            seg_img[:, :, 1] += ((seg[:, :] == c) * (colors[c][1])).astype('uint8')
            seg_img[:, :, 2] += ((seg[:, :] == c) * (colors[c][2])).astype('uint8')
    return seg_img


def visualize_segmentation_dataset(images_path, segs_path, n_classes, do_augment=False):
    img_seg_pairs = get_pairs_from_paths(images_path, segs_path)

    colors = class_colors

    print("Press any key to navigate. ")
    for im_fn, seg_fn in img_seg_pairs:
        img = cv2.imread(im_fn)
        seg = cv2.imread(seg_fn)
        print("Found the following classes", np.unique(seg))

        seg_img = np.zeros_like(seg)

        if do_augment:
            img, seg[:, :, 0] = augment_seg(img, seg[:, :, 0])

        for c in range(n_classes):
            seg_img[:, :, 0] += ((seg[:, :, 0] == c) * (colors[c][0])).astype('uint8')
            seg_img[:, :, 1] += ((seg[:, :, 0] == c) * (colors[c][1])).astype('uint8')
            seg_img[:, :, 2] += ((seg[:, :, 0] == c) * (colors[c][2])).astype('uint8')

        cv2.imshow("img", img)
        cv2.imshow("seg_img", seg_img)
        cv2.waitKey()


def visualize_segmentation_dataset_one(images_path, segs_path, n_classes, do_augment=False, no_show=False):
    img_seg_pairs = get_pairs_from_paths(images_path, segs_path)

    colors = class_colors

    im_fn, seg_fn = random.choice(img_seg_pairs)

    img = cv2.imread(im_fn)
    seg = cv2.imread(seg_fn)
    print("Found the following classes", np.unique(seg))

    seg_img = np.zeros_like(seg)

    if do_augment:
        img, seg[:, :, 0] = augment_seg(img, seg[:, :, 0])

    for c in range(n_classes):
        seg_img[:, :, 0] += ((seg[:, :, 0] == c) * (colors[c][0])).astype('uint8')
        seg_img[:, :, 1] += ((seg[:, :, 0] == c) * (colors[c][1])).astype('uint8')
        seg_img[:, :, 2] += ((seg[:, :, 0] == c) * (colors[c][2])).astype('uint8')

    if not no_show:
        cv2.imshow("img", img)
        cv2.imshow("seg_img", seg_img)
        cv2.waitKey()

    return img, seg_img


# from typing import
def visualize_anno(seg_img_path, n_classes=50, save_dir=None, show=False, colors=class_colors):
    txt_path=r'G:\Heart_Seg\A4C_B4C_P4C_image_filter.txt'
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

    seg = cv2.imread(seg_img_path)
    print("seg",seg.shape)
    print("Found the following classes", np.unique(seg))
    print(len(np.unique(seg)))
    '''if (len(np.unique(seg)))<5:
        print("seg_img_path",seg_img_path)
        str=seg_img_path.split("\\")
        f = open(txt_path,"a+")
        f.writelines(str[-1]+"\n")
        f.close()        '''


    seg_img = np.zeros_like(seg)
    for c in range(n_classes):
        seg_img[:, :, 0] += ((seg[:, :, 0] == c) * (colors[c][0])).astype('uint8')
        seg_img[:, :, 1] += ((seg[:, :, 0] == c) * (colors[c][1])).astype('uint8')
        seg_img[:, :, 2] += ((seg[:, :, 0] == c) * (colors[c][2])).astype('uint8')

    if save_dir:
        cv2.imwrite(os.path.join(save_dir, os.path.basename(seg_img_path)), seg_img)

    if show:
        cv2.imshow(os.path.basename(seg_img_path), seg_img)
        cv2.waitKey(0)


def visualize_in_triple(image, anno, pred, v_anno=True, v_pred=True, n_classes=50):
    """将原图，标注，预测结果拼接到一起进行可视化

    :param image: ndarry or str path of image
    :param anno: ndarry or str path of anno, it will be visualize only when v_seg is True
    :param pred:  ndarry or str path of predication, it will be visualize only when v_pred is True
    :param v_anno:
    :param v_pred:
    :return:
    """
    assert isinstance(image, str) or isinstance(image, np.ndarray)
    assert isinstance(anno, str) or isinstance(anno, np.ndarray)
    assert isinstance(pred, str) or isinstance(pred, np.ndarray)
    if isinstance(image, str):
        image = cv2.imread(image)
    if isinstance(anno, str):
        anno = cv2.imread(anno)
    if isinstance(pred, str):
        pred = cv2.imread(pred)
    if v_anno:
        anno = visualize_single_seg(anno, n_classes=n_classes, ignore_cls=None)
    if v_pred:
        pred = visualize_single_seg(pred, n_classes=n_classes, ignore_cls=None)
    h = sorted([image.shape[0], anno.shape[0], pred.shape[0]])[0]
    w = sorted([image.shape[1], anno.shape[1], pred.shape[1]])[0]
    stacked = np.hstack([cv2.resize(image, (w, h)), cv2.resize(anno, (w, h)), cv2.resize(pred, (w, h))])
    stacked = cv2.resize(stacked, (w * 3 // 2, h // 2))
    # cv2.imshow('stacked', stacked)
    # cv2.waitKey(0)
    ait = r'C:\Users\pb\Desktop\test_segemation'
    if not os.path.exists(ait):
        os.makedirs(ait)
    cv2.imwrite(os.path.join(ait, '{}.png'.format(len(os.listdir(ait)), )), stacked)
    print('writing ... ...')



def visualize_in_two(image,  pred, v_anno=True, v_pred=True, n_classes=50):
    """将原图，标注，预测结果拼接到一起进行可视化

    :param image: ndarry or str path of image
    :param anno: ndarry or str path of anno, it will be visualize only when v_seg is True
    :param pred:  ndarry or str path of predication, it will be visualize only when v_pred is True
    :param v_anno:
    :param v_pred:
    :return:
    """
    assert isinstance(image, str) or isinstance(image, np.ndarray)

    assert isinstance(pred, str) or isinstance(pred, np.ndarray)
    if isinstance(image, str):
        image = cv2.imread(image)
    if isinstance(pred, str):
        pred = cv2.imread(pred)
    print("image",image.shape)
    h = sorted([image.shape[0],  pred.shape[0]])[0]
    w = sorted([image.shape[1],  pred.shape[1]])[0]
    stacked = np.hstack([cv2.resize(image, (w, h)),  cv2.resize(pred, (w, h))])
    stacked = cv2.resize(stacked, (w * 2 // 2, h // 2))
    # cv2.imshow('stacked', stacked)
    # cv2.waitKey(0)
    ait = r'C:\Users\pb\Documents\WeChat Files\wxid_6764777647614\FileStorage\File\2020-07\lunao\connect'

    if not os.path.exists(ait):
        os.makedirs(ait)
    cv2.imwrite(os.path.join(ait, '{}.png'.format(len(os.listdir(ait)), )), stacked)
    print('writing ... ...')






def _vialize_all_anno(n_classes=50):
    """@ WareLee"""
    #seg_dir = r'C:\Users\pb\Desktop\test_chinese'
    save_dir = r'C:\Users\pb\Desktop\test_chinese3'

    seg_dir = r'C:\Users\pb\Desktop\test_save_A4C_480_352'
    save_dir = r'C:\Users\pb\Desktop\A4C_480_352_val'
    # tmp = [int(i) for i in np.linspace(0, 255, n_classes).tolist()]
    # colors = [(i, i, i) for i in tmp]
    # print(tmp)
    segg=r'E:/hnumedical/Heart_segmentation/Choose_A4C_SegFrame_label'
    save_dir1=r'E:/hnumedical/Heart_segmentation/Choose_A4C_SegFrame_label_show'

    for seg_name in os.listdir(segg):
        if seg_name.endswith(('.png', '.jpg', '.jpeg')):
            visualize_anno(os.path.join(segg, seg_name), save_dir=save_dir1, n_classes=n_classes, colors=class_colors)


def _vialize_dataset(default=50):
    """@ WareLee
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", type=str,
                        default=r'D:\datasets\seg_gugu_datasets\trainset\images')
    # default=r'D:\datasets\tmp\valset\images')
    parser.add_argument("--annotations", type=str,
                        default=r'D:\datasets\seg_gugu_datasets\trainset\labels')
    # default=r'D:\datasets\tmp\valset\labels')
    parser.add_argument("--n_classes", type=int, default=default)
    args = parser.parse_args()

    visualize_segmentation_dataset(args.images, args.annotations, args.n_classes)


def _visalize_multi_ds():
    """将颅脑和腹围的标注用一套色彩可视化，主要用于师兄的gan训练"""
    save_dir = r'D:\datasets\seg_vis_all\valset'

    folders = [r'D:\datasets\seg_lunao_datasets\valset', r'D:\datasets\seg_fuwei_datasets\valset']
    classes = [21, 12]
    index = 0
    tmp = [int(i) for i in np.linspace(0, 255, sum(classes) - len(classes) + 1).tolist()]
    class_colors = [(i, i, i) for i in tmp]
    # global class_colors
    bg = class_colors[0:1]
    class_colors = class_colors[1:]
    # class_colors = class_colors[1:]
    for i, folder in enumerate(folders):
        tp = classes[0:i]
        colors = bg + class_colors[sum(tp) - len(tp):sum(tp) - len(tp) + classes[i] - 1]
        # colors = bg + class_colors[sum(classes[0:i + 1]) - classes[i]:sum(classes[0:i + 1]) - 1]
        for name in os.listdir(os.path.join(folder, 'labels')):
            img_p = os.path.join(folder, 'images', name)
            label_p = os.path.join(folder, 'labels', name)
            shutil.copy(img_p, os.path.join(save_dir, 'images', '{}.png'.format(index)))
            seg = cv2.imread(label_p)
            seg_img = np.zeros_like(seg)
            for c in range(classes[i]):
                seg_img[:, :, 0] += ((seg[:, :, 0] == c) * (colors[c][0])).astype('uint8')
                seg_img[:, :, 1] += ((seg[:, :, 0] == c) * (colors[c][1])).astype('uint8')
                seg_img[:, :, 2] += ((seg[:, :, 0] == c) * (colors[c][2])).astype('uint8')
            cv2.imwrite(os.path.join(save_dir, 'vis', '{}.png'.format(index)), seg_img)
            index += 1


def gen_polygen_by_binimg(labels_dir):
    """
    将预测生成的label结果，结构化输出（以谭老师标注软件能解析的格式保存为annotations.json文件）

    :param labels_dir:
    :return:
    """
    clsnames = ['BG', '胼胝体', '透明隔', '丘脑', '第三脑室', '大脑镰', '侧脑室前角', '大脑实质', '侧脑室后角', '脉络丛', '颅骨光环', '脑岛', '大脑外侧裂', '穹窿柱',
                '透明隔腔',
                '颞上沟', '颞下沟', '顶枕沟', '额上沟', '扣带沟', '额下沟',
                '中脑', '小脑', '侧脑室体部', '胼胝体膝部', '胼胝体压部', '小脑半球']
    n_classes = len(clsnames)
    result = {"config": {
        "bodyPart": [
            {"name": "腹部", "subclass": [],
             "config": [{"name": "肝脏", "alias": "", "color": "200,100,200,128"},
                        {"name": "脊柱", "alias": "", "color": "255,0,0,128"},
                        {"name": "脐静脉及门静脉", "alias": "", "color": "255,128,0,128"},
                        {"name": "胃", "alias": "", "color": "255,255,0,128"},
                        {"name": "脾脏", "alias": "", "color": "0,255,0,128"},
                        {"name": "肾上腺", "alias": "", "color": "170,85,0,128"},
                        {"name": "下腔静脉", "alias": "", "color": "0,255,255,128"},
                        {"name": "降主动脉", "alias": "", "color": "255,0,255,128"},
                        {"name": "肋骨", "alias": "", "color": "85,0,255,128"},
                        {"name": "腹壁", "alias": "", "color": "255,85,127,128"},
                        {"name": "肾脏", "alias": "", "color": "215,194,255,128"},
                        {"name": "肺", "alias": "", "color": "96,170,0,128"}]},
            {"name": "股骨", "subclass": [],
             "config": [{"name": "股骨", "alias": "", "color": "200,100,200,128"},
                        {"name": "干骺端", "alias": "", "color": "255,0,0,128"}]},
            {"name": "肱骨", "subclass": [],
             "config": [{"name": "肱骨", "alias": "", "color": "200,100,200,128"},
                        {"name": "干骺端", "alias": "", "color": "255,0,0,128"}]},
            {"name": "丘脑", "subclass": [],
             "config": [{"name": "小脑蚓部", "alias": "", "color": "85,0,255,102"},
                        {"name": "胼胝体压部", "alias": "", "color": "85,0,255,102"},
                        {"name": "胼胝体膝部", "alias": "", "color": "85,0,255,102"},
                        {"name": "小脑", "alias": "", "color": "85,0,255,25"},
                        {"name": "小脑半球", "alias": "", "color": "85,0,255,102"},
                        {"name": "中脑", "alias": "", "color": "23,255,11,102"},
                        {"name": "侧脑室体部", "alias": "", "color": "0,255,127,25"},
                        {"name": "颅骨光环", "alias": "", "color": "255,170,255,128"},
                        {"name": "大脑镰", "alias": "", "color": "255,0,0,128"},
                        {"name": "大脑实质", "alias": "", "color": "255,170,127,25"},
                        {"name": "丘脑", "alias": "", "color": "0,85,255,128"},
                        {"name": "第三脑室", "alias": "", "color": "0,255,0,128"},
                        {"name": "侧脑室后角", "alias": "", "color": "0,0,255,128"},
                        {"name": "侧脑室前角", "alias": "", "color": "0,255,255,128"},
                        {"name": "脉络丛", "alias": "", "color": "255,255,255,128"},
                        {"name": "大脑外侧裂", "alias": "", "color": "85,0,255,128"},
                        {"name": "透明隔腔", "alias": "", "color": "255,85,127,128"},
                        {"name": "透明隔", "alias": "", "color": "255,85,255,128"},
                        {"name": "颞上沟", "alias": "", "color": "170,170,127,128"},
                        {"name": "颞下沟", "alias": "", "color": "85,170,255,128"},
                        {"name": "扣带沟", "alias": "", "color": "170,85,127,128"},
                        {"name": "穹窿柱", "alias": "", "color": "85,85,0,128"},
                        {"name": "额上沟", "alias": "", "color": "255,0,255,128"},
                        {"name": "顶枕沟", "alias": "", "color": "0,170,127,128"},
                        {"name": "距状沟", "alias": "", "color": "170,255,255,128"},
                        {"name": "胼胝体", "alias": "", "color": "255,170,127,128"},
                        {"name": "脑岛", "alias": "", "color": "170,0,127,128"},
                        {"name": "额下沟", "alias": "", "color": "255,203,219,128"}]},
            {"name": "侧脑", "subclass": [],
             "config": [{"name": "颅骨光环", "alias": "", "color": "255,170,255,128"},
                        {"name": "大脑镰", "alias": "", "color": "255,0,0,128"},
                        {"name": "大脑实质", "alias": "", "color": "255,128,0,128"},
                        {"name": "丘脑", "alias": "", "color": "255,255,0,128"},
                        {"name": "第三脑室", "alias": "", "color": "0,255,0,128"},
                        {"name": "侧脑室后角", "alias": "", "color": "0,0,255,128"},
                        {"name": "侧脑室前角", "alias": "", "color": "0,255,255,128"},
                        {"name": "脉络丛", "alias": "", "color": "255,85,0,128"},
                        {"name": "大脑外侧裂", "alias": "", "color": "85,0,255,128"},
                        {"name": "透明隔腔", "alias": "", "color": "255,85,127,128"},
                        {"name": "透明隔", "alias": "", "color": "255,85,255,128"},
                        {"name": "颞上沟", "alias": "", "color": "170,170,127,128"},
                        {"name": "颞下沟", "alias": "", "color": "85,170,255,128"},
                        {"name": "扣带沟", "alias": "", "color": "170,85,127,128"},
                        {"name": "穹窿柱", "alias": "", "color": "85,85,0,128"},
                        {"name": "额上沟", "alias": "", "color": "255,0,255,128"},
                        {"name": "顶枕沟", "alias": "", "color": "0,170,127,128"},
                        {"name": "距状沟", "alias": "", "color": "170,255,255,128"},
                        {"name": "胼胝体", "alias": "", "color": "255,170,127,128"},
                        {"name": "脑岛", "alias": "", "color": "170,0,127,128"}]},
            {"name": "小脑", "subclass": [],
             "config": [{"name": "颅骨光环", "alias": "", "color": "85,0,255,102"},
                        {"name": "大脑镰", "alias": "", "color": "255,0,0,128"},
                        {"name": "小脑半球", "alias": "", "color": "255,128,0,102"},
                        {"name": "小脑蚓部", "alias": "", "color": "255,255,0,102"},
                        {"name": "第四脑室", "alias": "", "color": "0,255,0,128"},
                        {"name": "大脑实质", "alias": "", "color": "255,170,255,0"},
                        {"name": "中脑", "alias": "", "color": "0,255,255,102"},
                        {"name": "丘脑", "alias": "", "color": "170,85,255,102"},
                        {"name": "第三脑室", "alias": "", "color": "255,85,0,128"},
                        {"name": "侧脑室前角", "alias": "", "color": "170,255,0,102"},
                        {"name": "大脑外侧裂", "alias": "", "color": "170,255,127,102"},
                        {"name": "透明隔腔", "alias": "", "color": "170,255,255,128"},
                        {"name": "透明隔", "alias": "", "color": "170,170,0,128"},
                        {"name": "颞上沟", "alias": "", "color": "0,255,127,128"},
                        {"name": "颞下沟", "alias": "", "color": "0,170,127,128"},
                        {"name": "扣带沟", "alias": "", "color": "170,170,255,128"},
                        {"name": "穹窿柱", "alias": "", "color": "255,85,127,102"},
                        {"name": "胼胝体", "alias": "", "color": "0,85,127,102"},
                        {"name": "脑岛", "alias": "", "color": "85,170,255,102"},
                        {"name": "海马", "alias": "", "color": "255,255,127,102"},
                        {"name": "小脑幕", "alias": "", "color": "170,0,0,102"},
                        {"name": "额上沟", "alias": "", "color": "0,0,0,128"},
                        {"name": "额下沟", "alias": "", "color": "85,170,127,128"},
                        {"name": "中脑导水管", "alias": "", "color": "255,0,255,128"},
                        {"name": "后颅窝池", "alias": "", "color": "0,85,255,102"},
                        {"name": "小脑延髓间隔", "alias": "", "color": "255,0,127,128"}]}
        ],
        "standard": ["标准", "基本标准", "非标准"],
        "info": []}}
    annotations = {}
    assert os.path.exists(labels_dir)
    for name in os.listdir(labels_dir):
        if name.endswith(('.png', '.jpg')):
            tmp = {"bodyPart": "丘脑", "subclass": "", "standard": "标准", "info": "",
                   "nstdreasons": {}, 'annotations': []}

            path = os.path.join(labels_dir, name)
            label = cv2.imread(path)[:, :, 0]
            parts = []
            for i in range(1, n_classes):
                # TODO 颅骨光环在findContours时，会变成实心的
                if clsnames[i] == '颅骨光环':
                    continue
                cur_mask = np.array(label == i, dtype=np.uint8)
                try:
                    _, contours, hierarchy = cv2.findContours(cur_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                except Exception as e:
                    contours, hierarchy = cv2.findContours(cur_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                if len(contours) > 0:
                    for cnt in contours:
                        part = {"type": 4, "name": clsnames[i], "alias": "", "color": "0,1,0", "start": "0,0",
                                "end": "0,0",
                                "zDepth": 0, "class": i, "vertex": ""}
                        # if len(cnt) < 8:
                        #     continue
                        vertex = ['{},{}'.format(p[0], p[1]) for p in np.squeeze(cnt, axis=1)]
                        part['vertex'] = ';'.join(vertex)
                        parts.append(part)
            tmp['annotations'] = parts
            annotations[name] = tmp
    result['annotations'] = annotations
    with open(os.path.join(labels_dir, 'annotations.json'), 'w', encoding='utf-8') as f:
        f.write(str(result).replace("'", '"'))


if __name__ == "__main__":
    # gen_polygen_by_binimg(r'C:\Users\WareLee\Desktop\temp\labels')

    # _vialize_dataset(default=11)
    # _vialize_dataset(default=3)
    # _vialize_all_anno(n_classes=21)

    # [0, 23, 46, 69, 92, 115, 139, 162, 185, 208, 231, 255]
    # _vialize_all_anno(n_classes=12)
    # [0, 12, 25, 38, 51, 63, 76, 89, 102, 114, 127, 140, 153, 165, 178, 191, 204, 216, 229, 242, 255]
    # _vialize_all_anno(n_classes=27)

    # _visalize_multi_ds()

    # seg = visualize_single_seg(r'D:\datasets\seg_lunao_datasets_dup\trainset\labels\22.png', 16, ignore_cls=None)
    # cv2.imshow('seg', seg)
    # cv2.waitKey(0)

    images = r'C:\Users\pb\Documents\WeChat Files\wxid_6764777647614\FileStorage\File\2020-07\lunao\orginal'
    #annos = r'C:\Users\pb\Desktop\test_segemation\trainset\labels'
    preds = r'C:\Users\pb\Documents\WeChat Files\wxid_6764777647614\FileStorage\File\2020-07\lunao\segemation'
    #for name in os.listdir(preds):
        #print(name)
        #print(os.path.join(images, name))
        #print(os.path.join(preds, name))
        #visualize_in_two(os.path.join(images, name), os.path.join(preds, name),n_classes=18, v_anno=False, v_pred=False)
    _vialize_all_anno()

