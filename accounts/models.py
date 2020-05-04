from django.db import models
from django.contrib.auth.models import (
      AbstractBaseUser,BaseUserManager
)

from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.template.loader import get_template #get_template associates the html strings with passed in context variables
from django.conf import settings
from django.db.models.signals import pre_save,post_save
from django.contrib.sites.models import Site
# Create your models here.

from ecommerce.utils import random_string_generator,unique_activation_key_generator



class UserManager(BaseUserManager):
      def create_user(self,email,password=None,is_staff=False,is_admin=False,is_active=True):
            if not email:
                  raise ValueError("Users must have an email address")
            if not password:
                  raise ValueError("Users must have password")
            user =self.model(
                  email=self.normalize_email(email),
            )
            user.set_password(password)
            user.staff =is_staff 
            user.admin =is_admin 
            user.active=is_active
            user.save(using=self._db)
            return user 

      def create_staffuser(self,email,password=None):
            user=self.create_user(email,password,is_staff=True)
            return user


      def create_superuser(self,email,password=None):
            user=self.create_user(email=email,password=password,is_admin=True,is_staff=True)
            return user




class User(AbstractBaseUser,PermissionsMixin):
      email=models.EmailField(unique=True,max_length=255)
      full_name=models.CharField(max_length=255,blank=True,null=True)
      active=models.BooleanField(default=True)
      is_active=models.BooleanField(default=True)
      staff=models.BooleanField(default=False)
      admin=models.BooleanField(default=False)


      USERNAME_FIELD='email'
      REQUIRED_FIELDS=['password']

      objects=UserManager() 

      def __str__(self):
            return self.email

      def get_full_name(self):
            return self.full_name


      def get_short_name(self):
            return self.email

      @property
      def is_staff(self):
            return self.staff


      @property
      def is_admin(self):
            return self.admin 

            
      @property
      def is_superuser(self):
            return self.admin







class EmailActivationForLogin(models.Model):
      user=models.ForeignKey(User,on_delete=models.CASCADE)
      email=models.EmailField()
      key=models.CharField(max_length=120,null=True,blank=True)
      activated=models.BooleanField(default=False)
      forced_expired=models.BooleanField(default=False)
      expires=models.IntegerField(default=7)
      timestamp=models.DateTimeField(auto_now_add=True)
      updated=  models.DateTimeField(auto_now=True)


      def __str__(self):
            return self.email



      def regenerate(self):
            self.key=None 
            self.save()
            if self.key is not None:
                  return True 
            else:
                  return False


      def send_activatation(self):
            if not self.activated and not self.forced_expired:
                  if self.key:
                        base_url=Site.objects.get_current().domain
                        path=f"{base_url}/account/activate_email/{self.key}"
                        context:{
                              "path":path,
                              "email":self.email
                        }
                        subject='1-Click Email varification'
                        txt_ = get_template('registration/emails/verify.txt').render(context)
                        html_=get_template('registration/emails/verify.html').render(context)
                        from_email='nurhasnatseam2@gmail.com'
                        receipient_list=[self.email]            
                        sent_mail=send_mail(
                              subject,
                              txt_,
                              from_email,
                              receipient_list,
                              html_message=html_,
                              fail_silently=False
                        )

                        return sent_mail
            return False



def pre_save_email_activation_for_login(sender,instance,*args,**kwargs):
      if not instance.activated and not instance.forced_expired:
            if not instance.key:
                  instance.key=unique_activation_key_generator(instance)


pre_save.connect(pre_save_email_activation_for_login,sender=EmailActivationForLogin)


def post_save_user_create_receiver(sender,instance,created,*args,**kwargs):
      if created:
            obj=EmailActivationForLogin.objects.create(user=instance,email=instance.email)
            obj.send_activation()

post_save.connect(post_save_user_create_receiver,sender=User)


class GuestEmail(models.Model):
      email=models.EmailField()
      active= models.BooleanField(default=True)
      update=models.DateTimeField(auto_now=True)
      timestamp=models.DateTimeField(auto_now_add=True)



      def __str__(self):
            return self.email 