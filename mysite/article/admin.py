from django.contrib import admin
from .models import ArticleColumn

# Register your models here.
#把栏目管理权限赋给超级管理员
class ArticleColumnAdmin(admin.ModelAdmin):
    list_display =('column','created','user')
    list_filter=('column',)
admin.site.register(ArticleColumn,ArticleColumnAdmin)

