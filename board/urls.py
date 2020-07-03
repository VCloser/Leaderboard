#!/usr/bin/env python
# -*- encoding=utf-8 -*-


from django.urls import re_path
from .views import BoardServerView

urlpatterns = [
    re_path(r'^server/$', BoardServerView.as_view()),
]
