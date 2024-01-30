from django import forms

from article.models import ArticlePost

from .models import ArticleColumn, Comment,ArticleTag


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
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("commentator","body",) #画面仅显示评论者和内容,其他字段不需要更新
#增加新tag        
class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ("tag",)        