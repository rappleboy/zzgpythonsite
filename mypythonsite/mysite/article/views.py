


import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from article.models import ArticlePost

from .forms import ArticlePostForm, ArticleColumnForm
from .models import ArticleColumn


# Create your views here.
@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):
    if request.method=="GET":
        #filter是两个语句合并, object.all(),然后根据user=request.user过滤条件
        #相当于Where语句 字符串结尾的写法是 filter(username_endswith="Zhao").order_by(user_id)
        #get如果没有结果返回异常报错 filter返回空
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form= ArticleColumnForm()
        return render(request,"article/column/article_column.html",{"columns":columns,'column_form':column_form})
    if request.method=="POST":
        column_name = request.POST['column']
        #通过查询 检查新名字是否已经存在
        columns = ArticleColumn.objects.filter(user_id=request.user.id,column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name)
            #ajax返回值
            return HttpResponse("1")
@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def rename_article_column(request):  
 
      
    column_id = request.POST['column_id']
    column_name = request.POST['new_name']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")
    
@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def del_article_column(request):  

      
    column_id = request.POST['column_id']

    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()

        return HttpResponse("1")
    except:
        return HttpResponse("0")
    
@login_required(login_url='/account/login/')
@csrf_exempt
def article_post(request):
    #发布文章
    if request.method=="POST":
        #使用post里参数填充form
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                #不提交,只通过save预处后生成db对象,form里面只有title和body内容
                new_article = article_post_form.save(commit=False)
                #
                new_article.author= request.user
                #article_post的外键定义中使用了related_name参数,所以可以使用uesr.article_column
                new_article.column = request.user.article_column.get(id=request.POST['column_id']) #column_id不属于ArticlePostForm的项目,需要独立取得
                #new_article.tag = request.user.tag.get(id=request.POST['tag_id'])
                new_article.save()
                #处理tags
                tags = request.POST['tags']

                
                if tags:
                    for atag in json.loads(tags):
                
                        tag=request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag) #多对多,add添加
                        new_article.save()
                
                return HttpResponse("0")
            except Exception as e:
                #db error
                return HttpResponse(e)
        else:
            #isvalid error
            return HttpResponse(article_post_form.errors)          
        
    if request.method=="GET":
        #get 显示
        article_post_form = ArticlePostForm()
        #增加标签显示
        articletags = request.user.tag.all()
        # user对象object的all(方法),外键定义中使用了related_name参数,所以可以使用uesr.article_column
        article_columns = request.user.article_column.all()
        return render(request,"article/column/article_post.html",{"article_post_form":article_post_form,"article_columns":article_columns,\
               "articletags":articletags})
@login_required(login_url='/account/login')      
def article_list(request):  
    msg = None
    #引入内置的分页功能
    articles = ArticlePost.objects.filter(author=request.user) #使用relatedname
    
    paginator = Paginator(articles,5) #初始化分页器 每页显示2条数据
    page = request.GET.get('page')#本次请求的页数
    try:

        current_page = paginator.page(page) #得到 指定page No的内容,必须大于0整数 ,不能为空否则异常
        articles = current_page.object_list
    except PageNotAnInteger:
        msg="PageNotAnInteger is not set"
        current_page = paginator.page(1)

        articles = current_page.object_list
    except EmptyPage:
        msg="EmptyPage"
        current_page = paginator.page(paginator.num_pages) #返回当前的页码
        articles = current_page.object_list
        # current_page.paginator.page_number
        
    
    return render(request,"article/column/article_list.html",{'articles':articles,'page':current_page,'msg':msg})
@login_required(login_url='/account/login')      
def article_detail(request,id,slug):  
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    #增加相同标签推荐文章
    #得到这个文章的标签列表
    article_tags_ids = article.article_tag.values_list(id,flat=True) #得到一个元组列表[(2,)(3,)],使用flat=True得到数组[2,3]
    print("*************article_tags_ids",article_tags_ids)
    #查询所有标签 in 标签列表的文章列表
    similar_articles=ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)#where id in ids and id <> currentid
    # 对一个列表加一列注释属性,属性名 same_tag, 值=count(tag)
    similar_articles = similar_articles.annotate(same_tag=Count("article_tag")).order_by('-same_tags','-created')[:4]
    print("*************similar_articles",similar_articles)
    return render(request,"article/column/article_detail.html",{'article':article,"similar_articles":similar_articles})

@login_required(login_url='/account/login')      
def article_test(request):  
    # article = get_object_or_404(ArticlePost,id=id,slug=slug)
    
    return render(request,"article/simple.html")

@login_required(login_url='/account/login')      
@csrf_exempt #必须加入豁免,否则会报403拒绝错误,因为没有注入csrf
def article_del(request):  
    # article = get_object_or_404(ArticlePost,id=id,slug=slug)
    article = ArticlePost.objects.get(id=request.POST['article_id'])
    try:
        article.delete()
        return HttpResponse("0")
    except:
        return HttpResponse("1")
    

    
#重新编辑文章   
@login_required(login_url='/account/login')          
@csrf_exempt #必须加入豁免,否则会报403拒绝错误,因为没有注入csrf
def article_edit(request,article_id):
    if request.method =="GET":
        article_columns=request.user.article_column.all()

        article_tags=request.user.tag.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title":article.title})
        this_article_column = article.column
        this_article_tags = article.article_tag.all()
        
        
        return render(request,"article/column/article_edit.html",{"this_article_form":this_article_form,"article_columns":article_columns,
                               "this_article_column":this_article_column,"this_article_tags":this_article_tags,"article":article,"article_tags":article_tags})
    # 填充form
    if request.method =="POST":
        #post
        try:
            article = ArticlePost.objects.get(id=article_id)
            article.column =request.user.article_column.get(id=request.POST['column_id'])
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            tags = request.POST['tags']
            if tags:
                for atag in json.loads(tags):
                    if len(article.article_tag.filter(tag=atag))>1:
                        pass
                    else:
                        tag=request.user.tag.get(tag=atag)
                        article.article_tag.add(tag) #多对多,add添加
                        article.save()
                        
            #成功0
            return HttpResponse("0")
        except Exception as e:
            return HttpResponse(e)
    

        