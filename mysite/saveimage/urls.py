# coding:utf-8
'''
Created on 2024年1月26日

@author: ZhiGangDLZhao
'''
from django.urls.conf import path

from . import views


urlpatterns=[
    path('list_images/',views.list_images,name="list_images"),
    path('upload_image/',views.upload_image,name='upload_image'),
    path('del_image/',views.del_image,name='del_image'),
    path('falls_images/',views.falls_images,name='falls_images'),    
    
    ]