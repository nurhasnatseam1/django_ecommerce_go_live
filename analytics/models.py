from django.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType 

# Create your models here.
from .utils import get_client_ip
from .signals import object_viewed_signal

User=settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
      user =models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=True,null=True)
      ip_address=models.CharField(max_length=222,blank=True,null=True)

      content_type=models.ForeignKey(ContentType,on_delete=models.DO_NOTHING) #Content Type is a list of models available in your project
      object_id=models.PositiveIntegerField() #instance id of the target model class

      content_object=GenericForeignKey('content_type','object_id')#content_obj = target instance of any model


      timestamp=models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return f"{self.content_obj} viewed at {self.timestamp}"

      class Meta:
            ordering=['-timestamp']
            verbose_name='Object Viewed'
            verbose_name_plural='Objects Viewed'
      



def object_viewed_receiver(sender,instance,request,*args,**kwargs):
      c_type=ContentType.objects.get_for_model(sender) #here sender = instance.__class__
      new_view_obj=ObjectViewed.objects.create(
            user=request.user,
            ip_address=get_client_ip(request),
            content_type=c_type,
            object_id=instance.id,
      )



object_viewed_signal.connect(object_viewed_receiver)
