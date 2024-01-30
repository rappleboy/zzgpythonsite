import django
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls.base import reverse
from django.utils import timezone

from slugify import slugify


# from django.utils import timezone
# Create your models here.
# 文章栏目类
class ArticleColumn(models.Model):
    def on_delete(self):
        pass
    #用户和文章栏目是1对多关系,一个用户可以设置多个文章栏目 多对多是ManyToManyField
    #通过ralated_name设定, 可以通过user.article_column来反向取得一个user拥有的所有column
    user = models.ForeignKey(User, related_name='article_column',on_delete=CASCADE)
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.column
    
class ArticleTag(models.Model): 
    #文章标签词典类 定义用户和自定义的tag 字段  
    author = models.ForeignKey(User, related_name="tag",on_delete=CASCADE)
    tag = models.CharField(max_length=500)
    def __str__(self):
        return self.tag    
    
class ArticlePost(models.Model):
    def ondelete(self):
        pass
    #外键连接 多对一个作者 可以通过user.article来反向取得一个user所有的文章
    author = models.ForeignKey(User, related_name="article",on_delete=CASCADE) #db 表字段是author_id
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    column = models.ForeignKey(ArticleColumn, related_name="article_column",on_delete=CASCADE)
    body = models.TextField()
    #增加一个文章所属tag的字段,是多对多关系,存放tag表的id ,这里用到了ArticleTag,需要在之前定义才能识别
    article_tag = models.ManyToManyField(ArticleTag, related_name="article_tag",blank=True)
    
    
    #多对多会增加一个表 article_articlepost_users_like
    user_like = models.ManyToManyField(User,related_name="article_like",blank=True)
    
    created = models.DateTimeField(default=timezone.now())#默认值是当地时间
    updated = models.DateTimeField(auto_now=True) #自动使用当前时间
    
    class Meta():
        #定义数据库表结构相关信息
        ordering=("title",) 
        index_together = (('id','slug'),) #嵌套元组数据 定义索引字段
    def __str__(self):
        return self.title
    
    def save(self,*args,**kargs): #参数有名字但元组类型不限制个数,0或多个,可以不指定名字 ,**必须每个参数都有keywords
        #重写save方法,增加一些数据预处理
        self.slug = slugify(self.title) #预先处理slug,调用父类保存
        super(ArticlePost, self).save(*args,**kargs)
    def get_absolute_url(self):
        #逆转解析url 得到文章的url路径
        #html中得到的路径是/article/article_detail/9Ce-Shi-markup/
        path = reverse("article:article_detail",args=[self.id, self.slug])

        return path
    def get_titles_url(self):
        #逆转解析url 得到文章的url路径
        #html中得到的路径是/article/article_detail/9Ce-Shi-markup/
        path = reverse("article:article_titles_detail",args=[self.id, self.slug])

        return path
#用户评论类    
class Comment(models.Model):
    def on_delete(self):
        pass
    #定义一个字段属性是artcile,外键连接关联ArticlePost类, 关联名称comments用户ArticlePost.object.comments引用所有连接类
    article = models.ForeignKey(ArticlePost, related_name='comments',on_delete=CASCADE)
    
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)#元组类, 符号按照倒叙排序
    
    def __str__(self):
        return "Comment by {0} on {1}".format(self.comentator.username,self.article)

    