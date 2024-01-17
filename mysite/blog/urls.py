"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from blog import views
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.urls import re_path



urlpatterns = [
    #这里路径相对于blog
    
    re_path(r'^$', views.blog_title,name='blog_title'), # 访问url,响应请求的函数,
    re_path(r'(?P<article_id>\d)/$', views.blog_article,name='blog_article'), # 访问url,响应请求的函数
    # path('blog/', views.blog_title,name='blog_title'), # 访问url,响应请求的函数,
    # path('/blog/1', views.blog_article,name='blog_article'), # 访问url,响应请求的函数,
]
