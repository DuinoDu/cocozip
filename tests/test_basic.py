# -*- coding: utf-8 -*-

from .context import cocozip

import unittest
import os
import cv2
from pycocotools.coco import COCO
from cocozip import torchvision
import time


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_imread(self):
        coco_anno = '/home/public_data/min.du/coco2017/annotations/instances_train2017.json'
        imgdir = '/home/public_data/min.du/coco2017/images/train2017'
        zip_file = '/home/public_data/min.du/coco2017/zip/train2017.zip'
        coco = COCO(coco_anno)
        image_ids = coco.getImgIds()
        for index in image_ids:
            file_name = '%012d.jpg' % index
            img = cocozip.imread(file_name, zip_file=zip_file)
            img2 = cv2.imread( os.path.join(imgdir, file_name) )
            print(img.shape, img2.shape)
            break

    def test_imread_hdfs(self):
        coco_anno = '/home/public_data/min.du/coco2017/annotations/instances_val2017.json'
        zip_file = 'hdfs://hobot-bigdata/user/min.du/gpu004/public/coco/zip/val2017.zip'
        coco = COCO(coco_anno)
        image_ids = coco.getImgIds()
        for index in image_ids[:100]:
            file_name = '%012d.jpg' % index
            img = cocozip.imread(file_name, zip_file=zip_file)
        os.system('rm val2017.zip')

    def test_imread_speed(self):
        coco_anno = '/home/public_data/min.du/coco2017/annotations/instances_train2017.json'
        imgdir = '/home/public_data/min.du/coco2017/images/train2017'
        zip_file = '/home/public_data/min.du/coco2017/zip/train2017.zip'
        coco = COCO(coco_anno)
        image_ids = coco.getImgIds()

        t1 = time.time()
        for index in image_ids[:1000]:
            file_name = '%012d.jpg' % index
            img = cocozip.imread(file_name, zip_file=zip_file)
        t2 = time.time()
        print('imread(zipfile): %f sec' % (t2 - t1))

        t1 = time.time()
        for index in image_ids[:1000]:
            file_name = '%012d.jpg' % index
            imgfile = os.path.join(zip_file+'@', file_name)
            img = cocozip.imread(imgfile)
        t2 = time.time()
        print('imread(zipfile, ignore first): %f sec' % (t2 - t1))


        t1 = time.time()
        for index in image_ids[:1000]:
            file_name = '%012d.jpg' % index
            img2 = cv2.imread( os.path.join(imgdir, file_name) )
        t2 = time.time()
        print('imread(imgdir): %f sec' % (t2 - t1))

    def test_CocoDetection(self):
        root = ''
        coco_anno = '/home/public_data/min.du/coco2017/annotations/instances_train2017.json'
        zip_file = '/home/public_data/min.du/coco2017/zip/train2017.zip'
        dataset = torchvision.CocoDetection(root, coco_anno, zip_file=zip_file)
        img, target = dataset[0]
        print(img.size)


if __name__ == '__main__':
    unittest.main()
