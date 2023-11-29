# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 00:33:54 2023

@author: 10364
"""

def CoupleFormulation(lib_lenth):
    xs, ys = [], []
    x0, y0 = 0.5, 0.2
    xs.append(x0)
    ys.append(y0)   
    
    for i in range(lib_lenth):
        x1 = 3.8*x0*(1.0-x0)-0.09*x0*y0      # Y→ X  0.09
        y1 = 3.8*y0*(1.0-y0)-0.01*y0*x0      # X → Y 0.01
        x0, y0 = x1, y1
        xs.append(x0)
        ys.append(y0)
        
    return xs, ys, "X", "Y"

L = 100000
data_x, data_y ,_ ,_ = CoupleFormulation(L)

import csv
# 创建或打开文件
csvfile = open('D:/Project/Python/paper/paper3/test.csv', mode='w', newline='')
# 标题列表
fieldnames = ['data_x', 'data_y']
# 创建 DictWriter 对象
write = csv.DictWriter(csvfile, fieldnames=fieldnames)
# 写入表头
write.writeheader()
# 写入数据
for i in range(L):
    write.writerow({'data_x': data_x[i], 'data_y': data_y[i]})