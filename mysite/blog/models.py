import django
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class BlogArticles(models.Model):
    # 作为表字段定义 ,每个类属性对应一个字段
    # 主题字段
    title = models.CharField(max_length=300)  # 主题
    # 作者 作者和用户的关系是外连接key ,
    author = models.ForeignKey(
        User, related_name="blog_posts", on_delete=django.db.models.deletion.CASCADE)
    # 内容
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now())
    # 定义

    class Meta:
        ordering = ("-publish",)  # 元组

    def __str__(self):
        return self.title
