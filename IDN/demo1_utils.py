#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import random 
import math
import sympy
from scipy.optimize import fsolve

def gen_clusters(cluster, cluster_point):           # 生成x、y坐标
    m0 = 0
    c0 = 5
    for i in range(cluster):
        mean = [m0, m0]
        cov = [[c0,0],[0,c0]]
        if i == 0:
            data = np.random.multivariate_normal(mean,cov,cluster_point[i])
        else:
            data = np.append(data, np.random.multivariate_normal(mean,cov,cluster_point[i]), 0)
        m0 += c0
    return data


def gen_label(cluster, cluster_point,label_list, error_rate):          # 生成 noisy label
    label = []
    for i in range(cluster):
        tmp = [label_list[i] for _ in range(cluster_point[i])]          # 原始label
        noise_list = random.sample(range(0, cluster_point[i]), int(cluster_point[i]*error_rate[i]))       # 随机添加noise
        for j in noise_list:
            tmp[j] = abs(1-tmp[j])
        label += tmp
    return label
    

def show_scatter(cluster, feat_cord, cluster_point):
    color = ["r","b","g"]
    tx, ty = 0, 0
    for i in range(cluster):
        x,y = feat_cord[tx:tx+cluster_point[0],0], feat_cord[ty:tx+cluster_point[0],1] 
        plt.scatter(x, y, s=10, c = color[i], alpha=0.6)
        plt.axis()
        plt.title("scatter")
        plt.xlabel("x")
        plt.ylabel("y")
        tx, ty = cluster_point[0], cluster_point[0]
    plt.show
    

def count_y123(feat_cord, label, cluster_sum):
    cnt = [0, 0, 0]
    temp_min = 1.0e+8
    rec_dis = [[0 for _ in range(cluster_sum)] for _ in range(cluster_sum)]
    record = [[-1, temp_min, -1, temp_min] for _ in range(cluster_sum)]
    
    # N * N
    for i in range(len(label)):
        if label[i]:
            cnt[0] += 1
        for j in range(len(label)):
            if i != j:
                # count distance
                if i < j:
                    rec_dis[i][j] = count_dis(feat_cord[i], feat_cord[j])
                elif i > j:
                    rec_dis[i][j] = rec_dis[j][i]
                # cnt_1
                if label[i]:
                    if rec_dis[i][j] < record[i][1]:
                        record[i] = [j, rec_dis[i][j] , record[i][0], record[i][1]]
                    elif rec_dis[i][j] < record[i][3]:
                        record[i] = [record[i][0], record[i][1], j, rec_dis[i][j] ]
        # cnt_2
        if label[i] and label[record[i][0]]:
            cnt[1] += 1
        # cnt_3
        if label[i] and label[record[i][0]] and label[record[i][2]]:
            cnt[2] += 1
    return cnt

                
def count_dis(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


def calc_func(p1, p2, p3):
    a, b, c = sympy.symbols('a b c')        # p, e+1, e-1
    res_all = sympy.solve([a * (1 - b) + (1-a) * c - p1,
                         a * (1 - b)**2 + (1-a)* c**2 - p2,  
                         a * (1 - b)**3 + (1-a)* c**3 - p3], 
                         [a, b, c])  
    return res_all


def calc_func_2(p1, p2, p3):
    def f(x):
        x0 = float(x[0])
        x1 = float(x[1])
        x2 = float(x[2])
        return [
            x0 * (1 - x1) + (1-x0) * x2 - p1,
            x0 * (1 - x1)**2 + (1-x0)* x2**2 - p2,  
            x0 * (1 - x1)**3 + (1-x0)* x2**3 - p3
        ]
    result = fsolve(f,[1, 1, 1])
    return result
    
#    
#def count_y1(label):                 
#    count = 0
#    list_1 = []
#    for i in range(len(label)):
#        if label[i] == 1:
#            count += 1
#            list_1.append(i)
#    return count, list_1
#    
#    
#def count_y23(list_1, feat_cord, label):            # y1=y2=1 ； y1=y2=y3=1
#    cnt_2, cnt_3 = 0, 0
#    min_dis =  1.0e+8
#    record = [[-1, min_dis, -1, min_dis] for _ in range(len(feat_cord))]     # 距离最近[序号、dis]；距离第二近[序号、dis]
#    list_2 = []
#    
#    # 先求出label+1中 距离最近&距离第二近 的序号和距离
#    tt = 0
#    for i in list_1:
#        tt += 1
#        for j in list_1:
#            if i != j:
#                dis = count_dis(feat_cord[i], feat_cord[j])
#                if dis < record[i][1]:
#                    record[i] = [j, dis, record[i][0], record[i][1]]
#                elif dis < record[i][3]:
#                    record[i] = [record[i][0], record[i][1], j, dis]
##        if tt % 100 == 0:
##            print(tt)
#    # 对label=+1中数据，看整体有没有距离更近的label=-1 
#    tt = 0
#    for i in list_1:
#        tt+= 1
#        for j in range(len(feat_cord)):
#            if i != j and (j not in list_1):        # label -1
#                dis = count_dis(feat_cord[i], feat_cord[j])
#                if dis < record[i][1]:
#                    record[i][0] = -1
#                    break
#                elif dis < record[i][3]:
#                    record[i][2] = -1
##        if tt % 100 == 0:
##            print(tt)
##    
#    # 记录不重复的 y1=y2=y3=1 数组
#    temp_3 = []
#    for i in list_1:
#        flag = 1
#        for j in [i, record[i][0], record[i][2]]:   # 3个都label=+1
#            if j == -1:
#                flag = 0
#                break
#        if flag:
#            repeat = 0
#            temp = {i, record[i][0], record[i][2]}
##            for t in temp_3:                # 判定重复否
##                if t == temp:
##                     repeat = 1
##                     break
#            if not repeat:
#                temp_3.append({i, record[i][0], record[i][2]})
#                cnt_3 = cnt_3+1           
#    # 根据record中数据，记录不重复的 y1=y2=1 数组
#    for rec in list_1:
#        rec_y = record[rec][0]
#        if rec_y != -1:
#            cnt_2 += 1 
#            list_2.append([rec, rec_y])
##            if record[rec_y][0] == rec:     # 如果互为min_dis，只计数1
##                record[rec_y][0] = -1    
#    return cnt_2, cnt_3
