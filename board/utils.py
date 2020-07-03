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
