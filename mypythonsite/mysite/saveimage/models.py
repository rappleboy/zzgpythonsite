from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from slugify import slugify


# Create your models here.
class SaveImage(models.Model):
    user=models.ForeignKey(User,related_name="images",on_delete=CASCADE)
    title=models.CharField(max_length=300)
    url=models.URLField() #继承charfield
    slug=models.SlugField(max_length=500,blank=True) #用在url显示上
    description = models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True,db_index=True) #设定索引字段
    image=models.ImageField(upload_to='images/%Y/%m%d') #定义上传图片指定文件夹 相对于document_root下的路径
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)#处理成拼音加_连接字符串
        super(SaveImage,self).save(*args,**kwargs)
