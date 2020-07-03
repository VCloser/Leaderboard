#!/usr/bin/env python
# -*- encoding=utf-8 -*-


from rest_framework import serializers

from .models import LeaderBoard


class BoardServerViewSerializer(serializers.ModelSerializer):
    '''
    排行榜序列化器
    '''
    score = serializers.IntegerField(min_value=1, max_value=10000000, required=True)

    class Meta:
        model = LeaderBoard
        fields = (
            'client_num',
            'score',
        )
        extra_kwargs = {
            'create_time': {'write_only': True},
        }
