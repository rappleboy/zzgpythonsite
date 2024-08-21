from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import SaveImageForm
from .models import SaveImage


# Create your views here.
@login_required(login_url='/account/user_login/')
@csrf_exempt #不是表单,需要豁免
@require_POST
def upload_image(request):
    #提交保存图片
    # ajax传来的数据是字典 {"title":title,"url":url,"description":description}
    form = SaveImageForm(data=request.POST) #使用字典类键值对填充form
    if form.is_valid():
        #数据验证成功
        try:
            new_item=form.save(commit=False)#先保存form中提交字段部分,返回model对象 image对象得到处理
            new_item.user=request.user #user得到处理
            new_item.save() #db 保存,增加slug得到处理
            return JsonResponse({'status':"0"})
        except Exception as e:
            print("********************",e)
            return JsonResponse({'status':"1","error":e.__str__()})
@login_required(login_url='/account/uesr_login')    
def list_images(request):    
    #显示所有图片
    images = SaveImage.objects.filter(user=request.user)
    return render(request,'saveimage/list_images.html',{'images':images})


#删除图片
@login_required(login_url='/account/user_login/')
@csrf_exempt #不是表单,需要豁免
@require_POST
def del_image(request):
    #提交保存图片
    img_id = request.POST['img_id']
    
    #数据验证成功
    try:
        image = SaveImage.objects.get(id=img_id)
        # image.image.path= 每个文件或图片文件都有path属性 upload_to设定相对路径
        # /home/zzg/mysite/mysite/media/images/2024/0127/shuimu.jpg
        image.delete()
        return JsonResponse({'status':"0"})
    except Exception as e:
        print("********************",e)
        return JsonResponse({'status':"1","error":e.__str__()})
    
def falls_images(request):
    images= SaveImage.objects.all()
    return render(request,'saveimage/falls_images.html',{'images':images})
            
