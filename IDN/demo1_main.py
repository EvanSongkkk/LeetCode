#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from demo1_utils import *
import time


if __name__ == '__main__':
    cluster = 2                                        # num of clusters
    cluster_sum = 1000
    p = 0.7
    error_rate = [0.2, 0.3]         # e-1 + e+1 < 1
    cluster_point = [int(cluster_sum*(1-p)), cluster_sum - int(cluster_sum*(1-p))]       # points in each cluster
    label_list = [i for i in range(cluster)]            # label-type
    
    # 数据生成
    feat_cord = gen_clusters(cluster, cluster_point)    # 生成一堆二维的点，生成两个高斯分布feat_cord
    show_scatter(cluster, feat_cord, cluster_point)
    noisy_label = gen_label(cluster, cluster_point, label_list, error_rate)    # 设定e+1=0.4，e-1=0.3和p=0.6,并打乱
    p1_r = round((p*(1-error_rate[1])**1 + (1-p) * error_rate[0]**1), 2)
    p2_r = round((p*(1-error_rate[1])**2 + (1-p) * error_rate[0]**2), 2)
    p3_r = round((p*(1-error_rate[1])**3 + (1-p) * error_rate[0]**3), 2)
    print("---------Real value---------")
    print(f"p1 = {p1_r}, p2 = {p2_r}, p3 = {p3_r}")
     
    # count
    t1 = time.time()
    cnt_1, cnt_2, cnt_3 = count_y123(feat_cord, noisy_label, cluster_sum)
    t2 = time.time()
    tm = t2-t1
    print("-----------Estimate------------")
    print(f"cnt_1 = {cnt_1}, cnt_2 = {cnt_2}, cnt_3 = {cnt_3}")
    # 求概率
    p1 = cnt_11 / cluster_sum
    p2 = cnt_22 / cluster_sum
    p3 = cnt_33 / cluster_sum
    print(f"p1 = {p1}, p2 = {p2}, p3 = {p3}")
    print(f"time_cost = {t2-t1} s")
    print("------------------------------\n")
    
    print("-----------Result------------")
    # 联立方程求p、e+1、e-1
    res = calc_func(p1, p2, p3)
    print("by_sympy: ", res)
    print("---------")
    res2 = calc_func_2(p1, p2, p3)
    print("by_fsolve: ", res2)
    

#    数noisy_label中y=1的
#    t1 = time.time()
#    cnt_1, list_1 = count_y1(noisy_label)            # label=+1的个数 & 序号
#    cnt_2, cnt_3 = count_y23(list_1, feat_cord, noisy_label)     # y1=1, y2=1  &  y1=1, y2=1, y3=1
#    print('cnt_1 = ', cnt_1)
#    print('cnt_2 = ', cnt_2)
#    print('cnt_3 = ', cnt_3)
#    t2 = time.time()
#    # 求概率
#    p1 = cnt_1 / cluster_sum
#    p2 = cnt_2 / cluster_sum
#    p3 = cnt_3 / cluster_sum
#    print(f"Estimate: p1 = {p1}, p2 = {p2}, p3 = {p3}")
#    tm = t2-t1
#    print(f"--------time_cost = {tm} s--------")
#    