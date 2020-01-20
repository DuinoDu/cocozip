"""
CocoDetection with zipfile
"""
import os
from PIL import Image
import cv2
import torchvision
from .io import imread


class CocoDetection(torchvision.datasets.coco.CocoDetection):
    def __init__(self, root, annFile,
                 transform=None,
                 target_transform=None,
                 transforms=None,
                 zip_file=None):
        super(CocoDetection, self).__init__(root, annFile,
                transform, target_transform, transforms)
        self.zip_file = zip_file
        if zip_file.startswith('hdfs://'):
            cmd = 'hdfs fs -get %s' % zip_file
            os.system(cmd)
            self.zip_file = os.path.basename(zip_file)

    def __getitem__(self, index):
        try:
            img, target = super(CocoDetection, self).__getitem__(index)
        except FileNotFoundError as e:
            coco = self.coco
            img_id = self.ids[index]
            ann_ids = coco.getAnnIds(imgIds=img_id)
            target = coco.loadAnns(ann_ids)

            path = coco.loadImgs(img_id)[0]['file_name']
            img = imread(path, zip_file=self.zip_file)
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            if self.transforms is not None:
                img, target = self.transforms(img, target)
        return img, target
