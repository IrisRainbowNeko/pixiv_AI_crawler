import json
import random
import os
import cv2
from tqdm import tqdm
from labeler import img_resize

n_test=50 # 测试集图像数量(每个类别)
set_raw='imset/cat_7.json' # 标签路径
img_root='pixiv_crawler/images/' # 原始图像路径
save_path='imset' # 划分后标签储存路径
img_save_path='imgs/' # 处理后图像储存路径

with open(set_raw, 'r', encoding='utf8') as f:
    data = json.load(f)

data_group=[[] for _ in range(3)]
data_group_test=[[] for _ in range(3)]
for k,v in tqdm(data.items()):
    img=cv2.imread(img_root+k)
    if img is None:
        continue
    if 0.4<=img.shape[0]/img.shape[1]<=2.5:
        data_group[v].append(k)
        cv2.imwrite(os.path.join(img_save_path,k), img_resize(img, width_new=448, height_new=448))
    else:
        print('Inappropriate shape:', img.shape[0]/img.shape[1])

for i,group in enumerate(data_group):
    print('group count:', len(group))
    test_g = random.sample(group, n_test)
    data_group_test[i].extend(test_g)
    for item in test_g:
        group.remove(item)

data_train = {item:cls for cls, group in enumerate(data_group) for item in group}
data_test= {item:cls for cls, group in enumerate(data_group_test) for item in group}

with open(os.path.join(save_path, 'train.json'), 'w', encoding='utf8') as f:
    json.dump(data_train, f, ensure_ascii=False)
with open(os.path.join(save_path, 'test.json'), 'w', encoding='utf8') as f:
    json.dump(data_test, f, ensure_ascii=False)