from django import forms
from .models import Course,Lesson

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model= Course
        fields=('title','overview') #form中创建2个字段用于输入,其他的有系统处理

class CreateLessonForm(forms.ModelForm):    
    class Meta:
        model = Lesson
        fields = ['course','title','video','description','attach']
    def __init__(self,user,*args,**kwargs):    
        #初始化函数提前把这个课的主题按照相同用户筛选出来
        super(CreateLessonForm,self).__init__(*args,**kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=user)