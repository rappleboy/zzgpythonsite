# coding:utf-8
'''
Created on 2024年1月24日

@author: ZhiGangDLZhao
'''



from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import redis

from article.forms import CommentForm, ArticleTagForm
from article.models import ArticlePost, Comment, ArticleTag


r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

#普通用户显示文章列表
def article_titles(request,authorname=None):
    #所有文章题目
    userinfo=None
    print("****************",authorname)
    if authorname:
        user = User.objects.get(username=authorname)
        articles_title=ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo#因为定义了一对一,每个user对象都一对一有一个userinfo对象,规定必须是类的小写名
            print("****************userinfo",userinfo)
        except:
            print("****************userinfoNone")
            userinfo = None
    else:
        
        articles_title=ArticlePost.objects.all()
        
    paginator = Paginator(articles_title,5)#分页器
    page = request.GET.get('page')
    msg = None
    # current_page = None
    
    try:
        current_page = paginator.page(page)
        
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:

        current_page = paginator.page(paginator.num_pages)#最大page数,属性,不是函数
    articles= current_page.object_list
    if not authorname:
        # 选择了某个作者
        print("@****************",authorname)
        return render(request,"article/list/article_titles.html",{"articles":articles,"page":current_page,"authorname":authorname})
        # 全部 
    else:
        
        return render(request,"article/list/article_titles_author.html",{"articles":articles,"page":current_page,"authorname":authorname,"userinfo":userinfo})

#阅读文章 ,可以点赞,加评论
def article_detail(request,id,slug):
    #增加访问量计数
    article= get_object_or_404(ArticlePost,id=id,slug=slug)    
    total_views = r.incr("article:{}:views".format(article.id))#定义增长键值 article:{id}:views
    
    
    #显示最热文章
    #amount设定的步长值,增加有序集合article_ranking中value的值, 这里是article.id每次每次调用加一
    
    r.zincrby('article_ranking',1,article.id)
    
    # 0,-1表示所有包含的元素,不确定大小, 按照实际存储值递减
    article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:10] #得到ranking对象前10个对象
    
    #得到数组,循环排名10的每个article id
    article_ranking_ids = [int(id) for id in article_ranking]
    
    #得到article对象列表
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids)) #双下划线 in条件
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id)) #排序按照每个文章对象x的的id在ranking ids中的序号进行排序
    
    
    if request.method == "POST":
        print("**************POST")
        # 如果是发表评论
        comment_form = CommentForm(data=request.POST)#使用post内容赋值data填充form内容
        if comment_form.is_valid():#检验数据合规
            new_comment = comment_form.save(commit=False)
            #form save()后生成一个DB 对象,之后添加其他form中没有的字段
            new_comment.article=article
            new_comment.save()
        comment_form = CommentForm();    

    else :

        #显示文章 get
        #增加相同标签推荐文章
        #得到这个文章的标签列表
        print("*************before article_tags_ids")
        article_tags_ids = article.article_tag.values_list("id",flat=True) #得到一个元组列表[(2,)(3,)],使用flat=True得到数组[2,3]
        print("*************article_tags_ids",article_tags_ids)
        #查询所有标签 in 标签列表的文章列表
        similar_articles=ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)#where id in ids and id <> currentid
        # 对一个列表加一列注释属性,属性名 same_tag, 值=count(tag)
        similar_articles = similar_articles.annotate(same_tag=Count("article_tag")).order_by('-same_tag','-created')[:4]
        print("*************similar_articles",similar_articles)
        comment_form = CommentForm();
    return render(request,"article/list/article_detail.html",{"article":article,"total_views":total_views,"most_viewed":most_viewed,"comment_form":comment_form,"similar_articles":similar_articles})
        
#普通用户显示文章列表
def xxxxxxxxxxxxxxxarticle_titles_author(request,authorname):
    #所有文章题目
    user = User.objects.get(username=authorname)
    articles_title=ArticlePost.objects.filter(author=user)
    paginator = Paginator(articles_title,5)#分页器
    page = request.GET.get('page')
    msg = None
    # current_page = None
    
    try:
        current_page = paginator.page(page)
        
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:

        current_page = paginator.page(paginator.num_pages)#最大page数,属性,不是函数
    articles= current_page.object_list
    
    return render(request,"article/list/article_titles_author.html",{"articles":articles,"page":current_page,'authorname':authorname})
    
#点赞处理
@login_required
@require_POST
@csrf_exempt    
def article_like(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    
    if article_id and action:
        try:
            #都入力了
            article = ArticlePost.objects.get(id=article_id)
            if action == 'like':
                #针对文档ID添加一个user_like关系
                article.user_like.add(request.user)
                return HttpResponse("1")    
            else:
                #取消点赞
                article.user_like.remove(request.user) 
                return HttpResponse("2")  
        except:
            return HttpResponse("error")
    
def article_comment(request):
        print("**************POST")
        #如果是发表评论
        # comment_form = CommentForm(data=request.POST)#使用post内容赋值data填充form内容
        # if comment_form.is_valid():#检验数据合规
        #     new_comment = comment_form.save(commit=False)
        #     #form save()后生成一个DB 对象,之后添加其他form中没有的字段
        #     new_comment.article=article
        #     new_comment.save()
        # comment_form = CommentForm();    
        
        #使用ajax方式
        article_id = request.POST.get("article_id")
        article = ArticlePost.objects.get(id=article_id)
        commentator = request.POST.get("commentator")
        body = request.POST.get("body")
        new_comment = Comment()
        new_comment.article=article
        new_comment.body = body
        new_comment.commentator = commentator
        new_comment.save()
        comment_form = CommentForm();
        return HttpResponse("1")
#增加打tag处理功能,ajax
@login_required(login_url="/account/user_login")  
@csrf_exempt
def article_tag(request):
        #get方法返回既有的和空form
        if request.method=="GET":
            articleTagForm = ArticleTagForm()
            articleTags =  request.user.tag.all()
            return render(request,'article/list/article_tag.html',{"articleTags":articleTags,"articleTagForm":articleTagForm})
        
        if request.method=="POST":
            #使用ajax方式
            tag = request.POST.get("tag")

            new_articleTag = ArticleTag()
            new_articleTag.tag=tag
            print("*********",request.user)
            new_articleTag.author = request.user

            
            new_articleTag.save()

            return HttpResponse("1")    
@login_required(login_url="/account/user_login")  
@csrf_exempt
@require_POST
def del_article_tag(request):
       
        if request.method=="POST":
            #使用ajax方式
            try:
                tag_id = request.POST.get("tag_id")
    
                articleTag = ArticleTag.objects.get(id=tag_id)
                
                articleTag.delete()
    
                return HttpResponse("0")   
            except:
                return HttpResponse("1")           
    
    