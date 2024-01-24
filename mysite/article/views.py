


from django.contrib.auth.decorators import login_required
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
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse("1")
            except:
                #db error
                return HttpResponse("2")
        else:
            #isvalid error
            return HttpResponse(article_post_form.errors)          
        
    if request.method=="GET":
        #get 显示
        article_post_form = ArticlePostForm()
        # user对象object的all(方法),外键定义中使用了related_name参数,所以可以使用uesr.article_column
        article_columns = request.user.article_column.all()
        return render(request,"article/column/article_post.html",{"article_post_form":article_post_form,"article_columns":article_columns})
@login_required(login_url='/account/login')      
def article_list(request):  
    articles = ArticlePost.objects.filter(author=request.user) #使用relatedname
    
    return render(request,"article/column/article_list.html",{'articles':articles})
@login_required(login_url='/account/login')      
def article_detail(request,id,slug):  
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    
    return render(request,"article/column/article_detail.html",{'article':article})

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
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title":article.title})
        this_article_column = article.column
        
        return render(request,"article/column/article_edit.html",{"this_article_form":this_article_form,"article_columns":article_columns,
                               "this_article_column":this_article_column,"article":article})
    # 填充form
    else:
        try:
            article = ArticlePost.objects.get(id=article_id)
            article.column =request.user.article_column.get(id=request.POST['column_id'])
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            #成功0
            return HttpResponse("0")
        except Exception as e:
            return HttpResponse(e)
    

        