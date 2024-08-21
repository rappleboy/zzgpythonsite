from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model): #model对应db,新建一个account_userprofile表 新建model后需要做migration数据生成表结构
    
    def delete(self):
        pass
    user = models.OneToOneField(User, unique=True,on_delete=delete)  # 一对一关系,必须唯一
    birth = models.DateField(blank=True, null=True)#自动验证日期格式,允许blank 允许true
    #EmailField URLFeild自动验证格式 fileField接受上传文件
    phone = models.CharField(max_length=20,null=True)
    
    def __str__(self): #定义私有函数
        return 'user {}'.format(self.user.username)
class UserInfo(models.Model):
    def delete(self):
        pass
    user = models.OneToOneField(User, unique=True,on_delete=delete)#和user对应
    school = models.CharField(max_length=100,blank=True)
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100,blank= True)
    aboutme = models.TextField(blank=True)#自我介绍text area,
    photo = models.ImageField(blank=True)
    def __str__(self):
        return "user:{}".format(self.user.username)#user是model里的变量
    
    

