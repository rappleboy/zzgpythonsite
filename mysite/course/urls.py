from django.urls.conf import path, re_path
from django.views.generic.base import TemplateView

from .views import AboutView, CreateLessonView,ListLessonsView
from .views import CourseListView, ManageCourseListView, CreateCourseView, DeleteCourseView


urlpatterns = [
    #没有直接使用 TemplateView（template_name=＂course/about.html＂）的方式
    #因为path中url解析只认识函数方式,不能解析实例化类的模式
    path('about/',AboutView.as_view(),name='about'),
    path('course_list/',CourseListView.as_view(),name='course_list'),
    path('manage_course/',ManageCourseListView.as_view(),name='manage_course'),
    path('create_course/',CreateCourseView.as_view(),name='create_course'),
    re_path('delete_course/(?P<pk>\d+)/',DeleteCourseView.as_view(),name='delete_course'),
    path('create_lesson/',CreateLessonView.as_view(),name='create_lesson'),
    re_path('list_lessons/(?P<course_id>\d+)/',ListLessonsView.as_view(),name='list_lessons'),
    re_path('detail_lesson/(?P<lesson_id>\d+)/',CreateLessonView.as_view(),name='detail_lesson'),
    
    ]