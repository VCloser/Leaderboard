#!/usr/bin/env python
# -*- encoding=utf-8 -*-


from django.db import models


class LeaderBoard(models.Model):
    '''
    玩家分数排行榜表
    '''
    client_num = models.IntegerField(verbose_name='客户端号')
    score = models.PositiveIntegerField(verbose_name='分数')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
