
from django import forms
from django.contrib.auth.models import User

from account.models import UserProfile, UserInfo


#登录时使用表单
class LoginForm(forms.Form):#继承
    username = forms.CharField() #输入框 type=text
    
    password = forms.CharField(widget=forms.PasswordInput)#widget规定密码输入框 type=password

    
#注册时使用表单
class RegistrationForm(forms.ModelForm): #继承Model表单 涉及到数据库操作
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)
    
    class Meta:
        #直接使用User model类,不需要新建,
        #内部类定义model数据更新到数据库哪个表,哪个字段     
        model = User #registerform 关联数据库 auth_user表,更新两个字段
        fields = ("username","email") #只需要更新两个字段
        #password已经作为model属性定义,不需要在这里追加
        
        #下面放在在调用表单.is_valid()时被调用 clean_+属性名称”命名方式所创建的方法，都有类似的功能
        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['passowrd2']:
                raise forms.ValidationError("passwords do not match")
                return cd['password2']
class UserProfileForm(forms.ModelForm):     
        
    class Meta():
        #meta类定义数据库相关
        model = UserProfile
        fields=("birth","phone")
class UserInfoForm(forms.ModelForm):
    #用户详细信息自我介绍表单
    class Meta:
        #form和db关系定义
        model = UserInfo
        #db要更新的字段
        fields=("school","company","profession","address","aboutme","photo")
class UserForm(forms.ModelForm):
    class Meta:
        #form和db关系定义
        model = User
        #user表单修改email ,但username不能修改,是唯一标识
        fields=("email",)
    
               
    
    
    
    