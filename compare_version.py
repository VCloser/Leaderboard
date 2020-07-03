#!/usr/bin/env python
# -*- encoding=utf-8 -*-

def compare_version(v1, v2):

    l1 = v1.split('.')
    l2 = v2.split('.')
    for i in range(max(len(l1), len(l2))):  # 循环最大位数
        if i >= len(l1) and int(l2[i]) != 0:  # b保证不出现index error
            return -1
        elif i >= len(l2) and int(l1[i]) != 0:
            return 1
        if i < len(l1) and i < len(l2):  # 当0超出 直接跳过
            if int(l1[i]) > int(l2[i]):
                return 1
            elif int(l1[i]) < int(l2[i]):
                return -1
    return 0
