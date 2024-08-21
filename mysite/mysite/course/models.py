from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from slugify import slugify
from .fields import OrderField

# Create your models here.
class Course(models.Model):
    user= models.ForeignKey(User,related_name="course_user",on_delete=CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)
    def save(self,*args,**kargs):
        self.slug = slugify(self.title)
        super(Course,self).save(*args,**kargs)
    def __str__(self):
        return self.title
def user_dir_path(instance,filename): #instance是一个实例
        return "courses/user_{0}/{1}".format(instance.user.id,filename)    
#课程类
class Lesson(models.Model):
    user=models.ForeignKey(User,related_name="lesson_user",on_delete=CASCADE)  
    course = models.ForeignKey(Course,related_name="lesson",on_delete=CASCADE) 
    title=models.CharField(max_length=200) 
    video=models.FileField(upload_to=user_dir_path) #定义相对文档根目录的子文件夹
    description = models.TextField(blank=True)
    attach= models.FileField(blank=True,upload_to=user_dir_path)
    created = models.DateTimeField(auto_now_add=True)
    order=OrderField(blank = True,for_fields=['course']) #目标字段是course,
    
    class Meta:
        ordering=['order']
    def __str__(self):
        return '{}.{}'.format(self.order,self.title)
    
    
    