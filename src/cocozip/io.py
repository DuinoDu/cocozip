# -*- coding: utf-8 -*-
import os
import zipfile
import cv2
import numpy as np


__all__ = ['imread']


_im_zfile = []


def imread(filename, flags=cv2.IMREAD_COLOR, zip_file=None):
    """
    Example: 
        xxx/train2017.zip@/000003945212.jpg
    or
        filename=00030300049.jpg, zipfile=xxx/train2017.zip

    You should zip train2017/xxxxx.jpg to train2017.zip.

    """
    global _im_zfile
    if zip_file is not None:
        path_zip = zip_file
        path_img = zip_file.split("/")[-1].split(".")[0] + '/' + filename
    else:
        path = filename
        pos_at = path.index('@')
        if pos_at == -1:
            print("character '@' is not found from the given path '%s'"%(path))
            assert 0
        zip_name = path.split("/")[-2].split(".")[0]
        path_zip = path[0: pos_at]
        path_img = zip_name + path[pos_at + 1:]

    if path_zip.startswith('hdfs://'):
        _path_zip = os.path.basename(path_zip)
        if not os.path.exists(_path_zip):
            cmd = 'hadoop fs -get %s' % path_zip
            print(cmd)
            os.system(cmd)
        path_zip = _path_zip

    if not os.path.isfile(path_zip):
        print("zip file '%s' is not found"%(path_zip))
        assert 0
    for i in range(len(_im_zfile)):
        if _im_zfile[i]['path'] == path_zip:
            data = _im_zfile[i]['zipfile'].read(path_img)
            return cv2.imdecode(np.frombuffer(data, np.uint8), flags)

    _im_zfile.append({
        'path': path_zip,
        'zipfile': zipfile.ZipFile(path_zip, 'r')
    })
    data = _im_zfile[-1]['zipfile'].read(path_img)

    return cv2.imdecode(np.frombuffer(data, np.uint8), flags)
