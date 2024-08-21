from urllib import request

from django import forms
from django.core.files.base import ContentFile
from slugify import slugify

from .models import SaveImage


class SaveImageForm(forms.ModelForm):
    class Meta:
        model = SaveImage
        #user,slug,image数据需要程序处理得到,不是form中提交 
        #slug在model中保存以前进行处理
        fields = ("title",'url','description')
        
    def clean_url(self):
        #固定命名方式 预处理某个字段值, clear+_+字段名
        #form.is_valid时候自动调用
        url=self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg','png']
        # 网址中分解除扩展名,从右方开始使用.分拆字符串,取得第2个内容
        extension = url.rsplit('.',1)[1].lower() #得到扩展名
        if extension not in valid_extensions:
            raise forms.ValidationError("the given url does not match valid image extension")
        return  url
    def save(self,force_insert=False,force_update=False,commit=True):
        saveimage=super(SaveImageForm,self).save(commit=False) #先保存,不提交到db
        image_url=self.cleaned_data['url']
        #使用原来的文件扩展名
        image_name = '{0}.{1}'.format(slugify(saveimage.title),image_url.rsplit('.',1)[1].lower())
        response = request.urlopen(image_url)
        #保存imagedata数据,从response中读取
        # response中存储图片二进制数据编码后的ascii码 ,保存成图片文件,路径在之前imagefield设定,继承fileField类,有保存文件的方法
        saveimage.image.save(image_name,ContentFile(response.read()),save=False)
        if commit:
            #正式提交保存db
            saveimage.save()
        return saveimage
            