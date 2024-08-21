from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required  # 修饰器
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse

from .forms import LoginForm
from .forms import RegistrationForm
from .forms import UserProfileForm, UserInfoForm, UserForm
from .models import UserInfo, UserProfile


# Create your views here.
def user_login(request):
    if request.method == "POST": #提交表单
        #给表单类传入字典类型的数据request.POST,建立一个绑定实例
        login_form = LoginForm(request.POST) #
        if login_form.is_valid():#验证入力值ok
            cd = login_form.cleaned_data
            #使用django的用户认证功能验证,得到user对象
            user = authenticate(username=cd["username"],password=cd["password"])
            
            if user: #不为空
                #调用django的login函数,在session中保存userid
                login(request, user)
                redirect_to='/home/'
                return HttpResponseRedirect(redirect_to)
            else:
                msg ="soryy your username or password is not right"
                return render(request,"account/login.html",{"form":login_form,"msg":msg})
                # return HttpResponse("soryy your username or password is not right")
        else:
            msg ="invalid login ,try agiain"
            # return HttpResponse("invalid login")
            return render(request,"account/login.html",{"form":login_form,"msg":msg})
    if request.method == "GET":
        login_form = LoginForm()#空对象,未绑定
        return render(request,"account/login.html",{"form":login_form})
# 定义注册新用户的试图函数
def user_register(request):  
    if request.method == "POST"  :
        user_form = RegistrationForm(request.POST)#使用post中参数列填充form
        userProfile_form = UserProfileForm(request.POST)
        if user_form.is_valid() * userProfile_form.is_valid():
            new_user = user_form.save(commit=False)#不保存到数据库,仅仅使用form值生成对象
            #追加设置要保存的字段 model中,forms中只设置了name和email反映到db字段上
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()#设定密码后调用save保存到数据库中
            new_userProfile = userProfile_form.save(commit=False)
            new_userProfile.user = new_user;
            new_userProfile.save()
            UserInfo.objects.create(user=new_user)#注册后,在userinfo表中插入新用户ID,其他信息为空
            
            # login_form = LoginForm()#空对象,未绑定
            # return render(request,"account/login.html",{"form":login_form,"message":"register successfully,please sign in"})
            # render(request, "account/login.html",{"form":user_form,"profile":userprofile_form})
            # return HttpResponse("successfully")
            redirect_to='/account/login/'
            if redirect_to == request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(reverse('account:user_login'))
            
        else:
            
            
            
            if not user_form.is_valid():
                print("****************",user_form.errors)
                return render(request, "account/register.html",{"errors":user_form.errors,"form":user_form,"profile":userProfile_form})
            if not userProfile_form.is_valid():
                print("****************",userProfile_form.errors)
                return render(request, "account/register.html",{"errors":userProfile_form.errors,"form":user_form,"profile":userProfile_form})
            # userProfile_form.
            #入力检查
            return HttpResponse("sorry you can not register.")
    else:
        #get 方法
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        # 使用空的对象,渲染文件register,使用form变量
        return render(request, "account/register.html",{"form":user_form,"profile":userprofile_form})
#修饰器函数  被修饰函数执行前被调用,判断是否已经登录  
@login_required(login_url='account/login/')
def myself(request):
    #用户个人信息的显示和更新
    user=User.objects.get(username=request.user.username)
    try:
        userInfo=UserInfo.objects.get(user=user)
    except:
        userInfo= UserInfo()
    try:
        userProfile=UserProfile.objects.get(user=user)
    except:
        userProfile= UserProfile()
    return render(request,"account/myself.html",{"user":user,"userInfo":userInfo,"userProfile":userProfile})

@login_required(login_url='account/login/')
def edit_myself(request):
    #用户个人信息更新 post提交数据, get原始数据显示
    user=User.objects.get(username=request.user.username)
    print("****************query user info",user.username)
    try:
        userInfo=UserInfo.objects.get(user=user)
    except:
        userInfo= UserInfo()
    try:
        userProfile=UserProfile.objects.get(user=user)
    except:
        userProfile= UserProfile()
    
    if request.method == "POST":
        print("****************method == POST",user.username)
        userForm = UserForm(request.POST)
        userProfileForm = UserProfileForm(request.POST)
        userInfoForm = UserInfoForm(request.POST)
        #入力数据检查
        if userForm.is_valid() * userProfileForm.is_valid() * userInfoForm.is_valid():
            #全部ok
            user_cd = userForm.cleaned_data
            userProfile_cd = userProfileForm.cleaned_data
            userInfo_cd = userInfoForm.cleaned_data
            user.email = user_cd['email']
            userProfile.user = request.user
            userProfile.birth=userProfile_cd['birth']
            userProfile.phone=userProfile_cd['phone']
            userInfo.user=request.user
            userInfo.school=userInfo_cd['school']
            userInfo.company=userInfo_cd['company']
            userInfo.profession=userInfo_cd['profession']
            userInfo.address=userInfo_cd['address']
            userInfo.aboutme=userInfo_cd['aboutme']
            user.save()
            userInfo.save()
            userProfile.save()
            #重定向 提交后当前url从/account/edit_my_information/转到/account/my_information/
            return HttpResponseRedirect('/account/my_information/')
        else:
            print(userForm.errors,userProfileForm.erros,userInfoForm.errors)
    else:
        print("****************method get")
        userForm = UserForm(instance=request.user)
        userProfileForm = UserProfileForm(initial={"birth":userProfile.birth,"phone":userProfile.phone})
        userInfoForm = UserInfoForm(initial={"school":userInfo.school,"company":userInfo.company,"profession":userInfo.profession,"address":userInfo.address,"aboutme":userInfo.aboutme})
        return render(request,"account/edit_myself.html",{"userForm":userForm,"userInfo":userInfoForm,"userProfile":userProfileForm})
    
@login_required(login_url='account/login/')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        userInfo = UserInfo.objects.get(user=request.user.id)
        userInfo.photo = img
        userInfo.save()
        return HttpResponse("1")
    else:
        return render(request,'account/imagecrop.html')