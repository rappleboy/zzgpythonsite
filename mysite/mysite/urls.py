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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.urls import re_path

from blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path(r'^admin/', admin.site.urls),
    # path('blog/', views.blog_title,name='blog_title'), # 访问url,响应请求的函数,
    re_path(r'^$', include(('blog.urls','blog'),namespace='blog')),
    re_path(r'blog/', include(('blog.urls','blog'),namespace='blog')),#appname=blog namespace='blog'
    #appname=blog namespace='blog'
    re_path(r'account/', include(('account.urls','account'),namespace='account')),
    re_path(r'^accounts/login/$', auth_views.LoginView.as_view(),name='user_login'),
    path("account/password_change_done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),#auth_view函数需要
    path("password_reset/", include(('password_reset.urls','password_reset'),namespace='password_reset')),
    path("article/", include(('article.urls','article'),namespace='article')),
    
    
]
