from django.urls import path
from django.urls.conf import re_path

from . import views  # 整个import views模块文件,而不是里面的某个类或函数


urlpatterns = [
    path('article_column',views.article_column,name="article_column"),
    path('rename_column',views.rename_article_column,name="rename_article_column"),
    path('del_column',views.del_article_column,name="del_article_column"),
    path('article_post',views.article_post,name="article_post"),
    path('article_list',views.article_list,name="article_list"),
    re_path(r'^article_detail/(?P<id>\d+)(?P<slug>[-\w]+)/$',views.article_detail,name="article_detail"),
    path('article_test',views.article_test,name="article_test"),
    path('article_del',views.article_del,name="article_del"),
    re_path(r'^article_edit/(?P<article_id>\d+)/$',views.article_edit,name="article_edit"),
    ]