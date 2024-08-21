from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.migrations.operations import fields


class OrderField(models.PositiveIntegerField): #继承正整数字段
    def __init__(self, for_fields=None,*args, **kwargs):
        self.for_fields = for_fields #定义一个目标字段, 针对某个字段取得序列号
        super(OrderField, self).__init__(*args,**kwargs)
    
    #保存之前对数据进行预先处理    
    def pre_save(self,model_instance, add): #model_instance实例对象,add为该示例第一次保存,不是update
        if getattr(model_instance,self.attname) is None: #当前对象是否有本字段,如果允许为空的情况为空,计算值,否则调用父类
            try: #不存在这个字段
                qs = self.model.objects.all() #取得当前实例的类的所有对象
                if self.for_fields: #定义了目标字段
                    query = {field:getattr(model_instance,field) for field in self.for_fields}
                    qs = qs.filter(**query) #根据目标字段的进行过滤
                last_item = qs.latest(self.attname) #得到最后一个order字段
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance,self.attname,value)
            return value
        else:
            return super(OrderField,self).pre_save(model_instance,add)
                
         