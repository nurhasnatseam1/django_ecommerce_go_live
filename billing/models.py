from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from accounts.models import GuestEmail
# Create your models here.



User=get_user_model()


#an unauthenticated user can have 100000 billing profiles
#but an authenticated user can only have one billing profile
#if an unauthenticated user having many billing profile gets authenticated for the first time
#then all his billing profile with the email should get deactivated

class BillingProfileManager(models.Manager):

      def new_or_get(self,request):
            user=request.user
            guest_email_id=request.session.get('guest_email_id')
            if user.is_authenticated:
                  if user.email:
                        billing_profile,billing_profile_created=self.model.objects.get_or_create(user=user,email=user.email)
            elif guest_email_id:
                  guest_email=GuestEmail.objects.filter(id=guest_email_id).order_by("-timestamp").first()
                  billing_profile,billing_profile_created=self.model.objects.get_or_create(email=guest_email.email)
            else:
                  billing_profile=None
                  billing_profile_created=None

            return billing_profile,billing_profile_created 
      



class BillingProfile(models.Model):
      user=models.ForeignKey(User,unique=True,on_delete=models.CASCADE,null=True,blank=True)
      email=models.EmailField()
      timestamp=models.DateTimeField(auto_now_add=True)
      updated=models.DateTimeField(auto_now=True)
      active=models.BooleanField(default=True)
      #customer id from stripe or brain tree
      
      
      
      objects=BillingProfileManager()
      def __str__(self):
            return self.email 

      



def user_created_receiver(sender,instance,created,*args,**kwargs):
      if created:
            BillingProfile.objects.get_or_create(user=instance,email=instance.email)


      return None 


post_save.connect(user_created_receiver,sender=User)