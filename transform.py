# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 01:11:58 2023

@author: 10364
"""

import h5py
data_path = 'D:/Project/Python/paper/paper3/hk_data_v1.mat'
data = h5py.File(data_path)	#得到的内容为HDF5 file
#可以使用data.keys()查看mat文件中各个cell   加入存在key为'X_train'
print(data.keys())
# 可以用values方法查看各个cell的信息
print(data.values())