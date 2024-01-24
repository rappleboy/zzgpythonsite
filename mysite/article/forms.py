from django import forms

from article.models import ArticlePost

from .models import ArticleColumn


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)#更新字段

#文章内容表单        
class ArticlePostForm(forms.ModelForm):      
    class Meta:
        #定义表单的meta数据
        model = ArticlePost
        fields=("title","body") #显示的字段