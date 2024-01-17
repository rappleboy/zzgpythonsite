from django.shortcuts import get_object_or_404
from django.shortcuts import render
import os

from .models import BlogArticles


# Create your views here.
def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, "blog/titles.html", {"blogs": blogs})

def blog_article(request,article_id):
    # article = BlogArticles.objects.get(id=article_id)
    
    print("*******************",article_id)
    # print("********************",os.path.join(BASE_DIR,'text'))
    article = get_object_or_404(BlogArticles,id=int(article_id))
    pub = article.publish
    #render渲染content.html,复制变量article和pub content中block使用
    return render(request,"blog/content.html",{"article": article,"publish": pub})
