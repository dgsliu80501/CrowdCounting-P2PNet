import os
import random
import torch
import numpy as np
from torch.utils.data import Dataset
from PIL import Image
import cv2
import glob
import scipy.io as io
class SHHA(Dataset):
    def __init__(self, data_root, transform=None, train=False, patch=False, flip=False):
        self.root_path = data_root
        self.train_lists = "DOTA_all_train.list"
        self.eval_list = "DOTA_all_test.list"
        # there may exist multiple list files
        self.img_list_file = self.train_lists.split(',')
        if train:
            self.img_list_file = self.train_lists.split(',')
        else:
            self.img_list_file = self.eval_list.split(',')

        self.img_map = {}
        self.img_list = []
        # loads the image/gt pairs
        for _, train_list in enumerate(self.img_list_file):
            train_list = train_list.strip()
            with open(os.path.join(self.root_path, train_list)) as fin:
                for line in fin:
                    if len(line) < 2: 
                        continue
                    line = line.strip().split()
                    self.img_map[os.path.join(self.root_path, line[0].strip())] = \
                                    os.path.join(self.root_path, line[1].strip())
        self.img_list = sorted(list(self.img_map.keys()))
        # number of samples
        self.nSamples = len(self.img_list)
        
        self.transform = transform
        self.train = train
        self.patch = patch
        self.flip = flip

    def __len__(self):
        return self.nSamples

    def __getitem__(self, index):
        assert index <= len(self), 'index range error'

        img_path = self.img_list[index]
        gt_path = self.img_map[img_path]
        # load image,ground truth and classes
        img, point, class_num = load_data((img_path, gt_path), self.train)
        # img, point = load_data((img_path, gt_path), self.train)
        # applu augumentation
        if self.transform is not None:
            img = self.transform(img)

        if self.train:
            # data augmentation -> random scale
            scale_range = [0.7, 1.3]
            min_size = min(img.shape[1:])
            scale = random.uniform(*scale_range)
            # scale the image and points
            if scale * min_size > 128:
                img = torch.nn.functional.upsample_bilinear(img.unsqueeze(0), scale_factor=scale).squeeze(0)
                point *= scale
        # random crop augumentaiton
        if self.train and self.patch:
            img, point ,class_num= random_crop(img, point, class_num)   # 经过随机crop之后point很多会变成空list, class_num也会改变
            for i, _ in enumerate(point):
                point[i] = torch.Tensor(point[i])
        # random flipping
        if random.random() > 0.5 and self.train and self.flip:
            # random flip
            img = torch.Tensor(img[:, :, :, ::-1].copy())
            for i, _ in enumerate(point):
                point[i][:, 0] = 128 - point[i][:, 0]

        if not self.train:
            point = [point]

        img = torch.Tensor(img)
        # pack up related infos
        target = [{} for i in range(len(point))]
        for i, _ in enumerate(point):
            # target[i]['class'] = torch.Tensor(class[i])
            target[i]['point'] = torch.Tensor(point[i])
            image_id = int(img_path.split('/')[-1].split('.')[0].split('_')[-1]) # TODO 这里的image_id得改
            image_id = torch.Tensor([image_id]).long()
            target[i]['image_id'] = image_id 
            # target[i]['labels'] = torch.ones([point[i].shape[0]]).long() # TODO 标签修改这里即可
            target[i]['labels'] = torch.Tensor(class_num[i])
        return img, target

# name to number
def name2num(name):
    if name == 'plane':
        return 1
    elif name == 'ship':
        return 2
    elif name == 'storage-tank':
        return 3
    elif name == 'baseball-diamond':
        return 4
    elif name == 'tennis-court':
        return 5
    elif name == 'basketball-court':
        return 6
    elif name == 'ground-track-field':
        return 7
    elif name == 'harbor':
        return 8
    elif name == 'bridge':
        return 9
    elif name == 'large-vehicle':
        return 10
    elif name == 'small-vehicle':
        return 11
    elif name == 'helicopter':
        return 12
    elif name == 'roundabout':
        return 13
    elif name == 'soccer-ball-field':
        return 14
    elif name == 'swimming-pool':
        return 15
    elif name == 'container-crane':
        return 16
    else:
        return 0

def load_data(img_gt_path, train): # TODO 加上读取目标的类别
    img_path, gt_path = img_gt_path
    # load the images
    img = cv2.imread(img_path)
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # load ground truth points
    points = []
    class_num = [] # TODO 加上读取目标的类别
    with open(gt_path) as f_label:
        for line in f_label:
            x = float(line.strip().split(' ')[0])
            y = float(line.strip().split(' ')[1])
            points.append([x, y])
            classes_name = str(line.strip().split(' ')[2])
            class_num.append(name2num(classes_name))
    # return img, np.array(points), np.array(class)
    return img, np.array(points), np.array(class_num)

# random crop augumentation
def random_crop(img, den, class_num, num_patch=4): # TODO 删除没有目标的文件才能不报错
    half_h = 128  # 更改crop_size, 原128
    half_w = 128  # 更改crop_size, 原128
    result_img = np.zeros([num_patch, img.shape[0], half_h, half_w])
    result_den = []
    result_num = []
    # crop num_patch for each image
    for i in range(num_patch):
        start_h = random.randint(0, img.size(1) - half_h)
        start_w = random.randint(0, img.size(2) - half_w)
        end_h = start_h + half_h
        end_w = start_w + half_w
        # copy the cropped rect
        result_img[i] = img[:, start_h:end_h, start_w:end_w]
        # copy the cropped points
        idx = (den[:, 0] >= start_w) & (den[:, 0] <= end_w) & (den[:, 1] >= start_h) & (den[:, 1] <= end_h) 
        # shift the corrdinates
        record_den = den[idx]
        record_num = class_num[idx]
        record_den[:, 0] -= start_w # 减去crop的起始点
        record_den[:, 1] -= start_h

        result_den.append(record_den)
        result_num.append(record_num)

    return result_img, result_den, result_num