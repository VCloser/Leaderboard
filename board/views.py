#!/usr/bin/env python
# -*- encoding=utf-8 -*-


from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import api_response
from .serializers import BoardServerViewSerializer
from .models import LeaderBoard


class BoardServerView(APIView):
    '''
    上传分数和查看排行
    '''

    def get(self, request):
        '''
        排行
        '''
        client_num = request.META.get('HTTP_X_CLIENT_NUM')
        page = request.query_params.get('page')
        if not all((page, client_num)):  # 参数校验
            res_data = api_response(errcode=10000, data='参数错误')
            return Response(data=res_data)
        page = int(page)
        if page < 1:
            res_data = api_response(errcode=10000, data='参数错误')
            return Response(data=res_data)
        client_num = int(client_num)
        offset = (page - 1) * settings.SIZE
        _sql_limit = f'SELECT id, client_num, score FROM ' \
                     f'( SELECT id, client_num, score FROM board_leaderboard ORDER BY create_time DESC ) ' \
                     f'AS b GROUP BY b.client_num ORDER BY b.score DESC LIMIT %s OFFSET %s'
        queryset = LeaderBoard.objects.raw(_sql_limit, params=[settings.SIZE, offset])
        if not queryset:
            res_data = api_response(data=[])
            return Response(data=res_data)
        serializer = BoardServerViewSerializer(queryset, many=True)
        res_data = serializer.data
        search_client_msg = None
        response_data = []
        for index_, client_msg in zip(range((page - 1) * settings.SIZE + 1, page * settings.SIZE + 1), res_data):
            client_n = client_msg['client_num']
            res_msg = {
                'order': index_,
                'client': f'客户端{client_n}',
                'score': client_msg['score']
            }
            if client_num == client_n:
                search_client_msg = res_msg
            response_data.append(res_msg)
        if search_client_msg is None:
            _sql = f'SELECT id, client_num, score FROM ' \
                   f'( SELECT id, client_num, score FROM board_leaderboard ORDER BY create_time DESC ) ' \
                   f'AS b GROUP BY b.client_num ORDER BY b.score DESC'
            queryset = LeaderBoard.objects.raw(_sql)
            for order, query in enumerate(queryset, start=1):
                if client_num == query.client_num:
                    res_msg = {
                        'order': order,
                        'client': f'客户端{query.client_num}',
                        'score': query.score
                    }
                    search_client_msg = res_msg
                    break
            else:
                res_list_data = api_response(errcode=10003, data=f'找不到客户端{client_num}')
                return Response(data=res_list_data)
        response_data.append(search_client_msg)
        res_list_data = api_response(data=response_data)
        return Response(data=res_list_data)

    def post(self, request):
        '''
        提交分数
        '''
        client_num = request.META.get('HTTP_X_CLIENT_NUM')
        score = request.data.get('score')
        if not all((client_num, score)):
            res_data = api_response(errcode=10000, data='参数错误')
            return Response(data=res_data)
        req_data = {
            'client_num': client_num,
            'score': score
        }
        serializer = BoardServerViewSerializer(data=req_data)
        if serializer.is_valid():
            serializer.save()
            res_data = api_response()
        else:
            res_data = api_response(errcode=10001, data=serializer.errors)
        return Response(data=res_data)
