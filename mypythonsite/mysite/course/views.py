import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView, View, TemplateResponseMixin
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from .forms import CreateCourseForm, CreateLessonForm
from .models import Course, Lesson


# Create your views here.
class AboutView(TemplateView):
    template_name="course/about.html"
    
class CourseListView(ListView):
    model = Course #list数据是course的所有数据
    context_object_name="courses" #定义传入模板网页的变量名称,如果没有定义默认是object
    template_name="course/course_list.html"
    
class UserMixin:  #默认继承Object类
    def get_queryset(self):
        qs = super(UserMixin,self).get_queryset()
        return qs.filter(user=self.request.user)
    
class UserCourseMixin(UserMixin,LoginRequiredMixin): #继承
    model = Course
    login_url='/account/login/'
    
class ManageCourseListView(UserCourseMixin,ListView):#继承,有queryset和model=course变量
    context_object_name = "courses"
    template_name='course/manage/manage_course_list.html'
    
class CreateCourseView(UserCourseMixin,CreateView):      #继承关联course 和自动登录功能,CreateView自动创建新form响应GET方法
    fields=['title','overview']  #create view专用设定
    template_name='course/manage/create_course.html' 
    
    def post(self,request,*args,**kargs):
        form = CreateCourseForm(data=request.POST) #根据用户入力数据填充
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user= request.user
            new_course.save()
            return redirect("course:manage_course")  #成功后重定向
        return self.render_to_response({'form':form}) #使用form 返回原来请求路径 重新填写
    
    
class DeleteCourseView(UserCourseMixin,DeleteView):
    
    #get方法根据url中pk参数 生成对象form迁移到confirm.html
    #pk = self.kwargs.get(self.pk_url_kwarg)
    #删除确认模板
    template_name='course/manage/delete_course_confirm.html'
    #POST处理删除成功后迁移path
    success_url=reverse_lazy("course:manage_course")
    
    # def post(self, request, *args, **kwargs):
    #     print("**********kwargs",kwargs)
    #     return super(DeleteCourseView,self).post(request, *args, **kwargs)
    
    def dispatch(self, *args, **kwargs):
        #原本DeleteView执行dispatch后重定向到success_url,重写后截取response,返回json result=OK,ajax处理
        resp = super(DeleteCourseView,self).dispatch(*args,**kwargs)
        if self.request.is_ajax:
            
            response_data = {"result":"ok"}
            return HttpResponse(json.dumps(response_data),content_type="application/json")
        else:
            return resp
        
        
class CreateLessonView(LoginRequiredMixin,View):    
    model = Lesson
    login_url="/account/user_login/"
    
    def get(self,request,*args,**kwargs):
        form = CreateLessonForm(user=self.request.user)
        return render(request,"course/manage/create_lesson.html",{'form':form})
    
    def post(self,request,*args,**kwargs):
        #user,*args,**kwargs):   
        form = CreateLessonForm(self.request.user,request.POST,request.FILES)
        #自动根据字段名填充form
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user=self.request.user
            new_lesson.save()
            return redirect("course:manage_course")
        
class ListLessonsView(LoginRequiredMixin,TemplateResponseMixin,View):    
    login_url = "/account/user_login"
    template_name='course/manage/list_lessons.html'    
    
    #根据课程id取得课程对象,html中课程对象的所有上课内容
    def get(self,request,course_id):   
        course = get_object_or_404(Course,id=course_id)
        return self.render_to_response({'course':course})
        
    