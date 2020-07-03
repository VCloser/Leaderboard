#!/usr/bin/env python
# -*- encoding=utf-8 -*-


def api_response(errcode=0, data=None):
    '''
    API返回格式
    '''
    if data is None:
        data = {}

    return {
        'errcode': errcode,
        'data': data,
    }

def binary_search(sql_list, client_num):
    '''
    二分查找查询的客户端
    :param sql_list:
    :param client_num:
    :return: 返回index+ 1， 查询信息
    '''
    low = 0
    high = len(sql_list) - 1
    origin_list = [i.client_num for i in sql_list]
    sorted_list = sorted(sql_list, key=lambda x: x.client_num)
    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid].client_num == client_num:
            return origin_list.index(client_num) + 1, sorted_list[mid]
        elif sorted_list[mid].client_num > client_num:
            high = mid - 1
        else:
            low = mid + 1
    return -1, None
