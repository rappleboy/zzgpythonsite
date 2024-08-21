

from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import re_path

from . import views


# from django.contrib.admin import views as auth_views
urlpatterns = [
    re_path(r'^login/$', views.user_login,name='user_login'), # 访问url,响应请求的函数,
    #使用django内置的登录功能
    # re_path(r'^login/$', auth_views.LoginView.as_view(),name='user_login'), # 访问url,响应请求的函数,
    # path("login/", auth_views.LoginView.as_view(), name="user_login")
    # re_path('newlogin', auth_views.LoginView.as_view(),name='user_login'), # 访问url,响应请求的函数,
    # path("newlogin/", auth_views.LoginView.as_view(), name="user_login")
    re_path(r'^logout/$', auth_views.LogoutView.as_view(),name='user_logout'),
    path("register/", views.user_register, name="user_register"),
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change_done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/",auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm",),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete",),
    path("my_information/",views.myself,name='my_information'),
    path("edit_my_information/",views.edit_myself,name='edit_my_information'),
    path("my_image/",views.my_image,name='my_image'),
    ]