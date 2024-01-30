#统计文章总数等模板标签tag的定义文件
from django import template  # 引入模板库 在__init__定义所有类和方法
from django.contrib.auth.models import User
from django.db.models.aggregates import Count

from article.models import ArticlePost


register = template.Library() #__init__中定义的公开class

@register.simple_tag #修饰器 表明下面的代码是自定义的simple_tag类型的模板标签
def total_articles():
    #标签的功能
    return ArticlePost.objects.count()

@register.simple_tag #修饰器 表明下面的代码是自定义的simple_tag类型的模板标签
def author_total_articles(authorname):
    #标签的功能
    return User.objects.get(username=authorname).article.count()

#最新发布的文章
@register.inclusion_tag('article/list/latest_articles.html') #设定要渲染的模板文件
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by("-created")[:n]#按照创建时间降序,取前n个list
    #对于inclusion_tag类型标签,设定渲染对象html后返回字典对象展现 
    return {"latest_articles":latest_articles} #返回字典对象

#评论最多的文章list
@register.simple_tag
def most_commented_articles(n=3):
    # 使用annotate给每个object进行标注,使用Count('comments'),每个对象都增加一个属性total_comments, comments是articlepost表的外键关联名
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")[:n]#注解total_comments的值的降序
    
