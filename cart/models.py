from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed,pre_save
# Create your models here.

from products.models import Product

User=get_user_model()

class CartModelManager(models.Manager):
      def new(self,user=None):
            user_obj=None 
            if user is not None:
                  if user.is_authenticated:
                        user_obj=user
            return self.model.objects.create(user=user_obj)


      def new_or_get(self,request):
            
            cart_id=request.session.get("cart_id")

            qs=Cart.objects.filter(id=cart_id)
            if qs.count()==1:
                  print("cart id exists")
                  cart_obj=qs.first()
                  new_obj=False
                  if request.user.is_authenticated and cart_obj.user is None:
                        cart_obj.user =request.user
                        cart_obj.save()
            else:
                  cart_obj=Cart.objects.new(user=request.user)
                  new_obj=True
                  request.session['cart_id']=cart_obj.id
            return cart_obj,new_obj
class Cart(models.Model):
      products=models.ManyToManyField(Product,related_name='carts')
      total=models.DecimalField(default=0.0,decimal_places=2,max_digits=10)
      subtotal=models.DecimalField(default=0.0,decimal_places=2,max_digits=10)
      user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) ##so that unautheticated users can create cart
      timestamp=models.DateTimeField(auto_now_add=True)
      updated=models.DateTimeField(auto_now=True)


      objects=CartModelManager()
      def __str__(self):
            return  str(self.id) 






def cart_products_changed(sender,instance,action,*args,**kwargs):
      if action in ['post_add','post_remove','post_clear']:
            print("i am here")
            products=instance.products.all()
            total=0
            for x in products:
                  total+=x.price
            print(total)
            if instance.subtotal!=total:
                  instance.subtotal=total
                  instance.save()
   


m2m_changed.connect(cart_products_changed,sender=Cart.products.through)



def pre_save_cart_receiver(sender,instance,*args,**kwargs):
      supply_cost=10
      if instance.subtotal>0:
            instance.total=instance.subtotal+supply_cost; 
      else:
            instance.total=0.0

pre_save.connect(pre_save_cart_receiver,sender=Cart)