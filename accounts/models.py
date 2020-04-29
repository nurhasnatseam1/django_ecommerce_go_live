from django.db import models
from django.contrib.auth.models import (
      AbstractBaseUser,BaseUserManager
)
from django.contrib.auth.models import PermissionsMixin
# Create your models here.

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

      @property 
      def is_active(self):
            return self.active






class GuestEmail(models.Model):
      email=models.EmailField()
      active= models.BooleanField(default=True)
      update=models.DateTimeField(auto_now=True)
      timestamp=models.DateTimeField(auto_now_add=True)



      def __str__(self):
            return self.email 