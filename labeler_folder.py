import os
import cv2
import numpy as np
import json
from tqdm import tqdm
from copy import deepcopy
from pathlib import Path

img_exts=['jpg', 'png', 'jpeg', 'bmp', 'tif']

def img_resize(image, width_new = 1280, height_new = 720):
    height, width = image.shape[0], image.shape[1]
    # 设置新的图片分辨率框架
    # 判断图片的长宽比率
    if width / height >= width_new / height_new:
        img_new = cv2.resize(image, (width_new, int(height * width_new / width)))
    else:
        img_new = cv2.resize(image, (int(width * height_new / height), height_new))
    return img_new

def make_label(root, save_path):
    label_dict={}
    root=Path(root)

    cls_list=list(filter(lambda x:os.path.isdir(root / x), os.listdir(root)))

    for i, cls in enumerate(cls_list):
        imgs=os.listdir(root / cls)
        for img in imgs:
            if img[img.rfind('.')+1:].lower() in img_exts:
                label_dict[os.path.join(cls, img)] = i

    with open(save_path, 'w', encoding='utf8') as f:
        json.dump(label_dict, f, ensure_ascii=False)
    return label_dict

if __name__ == '__main__':
    root='images_group/' #图像文件夹路径
    label_dict=make_label(root, 'dataset.json')