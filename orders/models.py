from django.db import models
from django.db.models.signals import pre_save,post_save
import math
from decimal import Decimal
# Create your models here.
from billing.models import BillingProfile
from cart.models import Cart
from ecommerce.utils import unique_order_id_generator
from address.models import Address
ORDER_STATUS_CHOICES=(
      ('created','Created'),
      ('shipped','Shipped'),
      ('paid','Paid'),
      ('refunded',"Refunded"),
)

class OrderManager(models.Manager):

      def new_or_get(self,billing_profile,cart_obj):
            order_qs = self.get_queryset().filter(cart=cart_obj,active=True,billing_profile=billing_profile,status="created")
            if order_qs.count()==1:
                  order_obj=order_qs.first()
                  new=False
            else: 
                  order_obj=self.model.objects.create(billing_profile=billing_profile,cart=cart_obj)
                  new=True
            return order_obj,new

class Order(models.Model):
      order_id = models.CharField(max_length=120,blank=True)
      billing_profile=models.ForeignKey(BillingProfile,on_delete=models.DO_NOTHING,null=True,blank=True)
      shipping_address=models.ForeignKey(Address,on_delete=models.DO_NOTHING,related_name='shipping_associated_orders',null=True,blank=True)
      billing_address=models.ForeignKey(Address,on_delete=models.DO_NOTHING,related_name="billing_associated_orders",null=True,blank=True)
      cart=models.ForeignKey(Cart,on_delete=models.DO_NOTHING,related_name='order')
      status=models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
      shipping_total=models.DecimalField(decimal_places=2,max_digits=10,default=10.0)
      order_total=models.DecimalField(decimal_places=2,max_digits=10,default= 0.0)
      active=models.BooleanField(default=True)


      objects=OrderManager()

      def __str__(self):
            return self.order_id


      def update_total(self):
            print('in update total')
            cart_total=self.cart.total
            new_total=math.fsum([Decimal(cart_total)+Decimal(self.shipping_total)])
            formated_total=format(new_total,'.2f')
            self.order_total=formated_total 
            self.save()
            return self.order_total


      def check_done(self):
            billing_profile=self.billing_profile
            shipping_address=self.shipping_address
            billing_address=self.billing_address 
            total=self.order_total 
            if total < 0:
                  return False 
            elif billing_profile and shipping_address and billing_address and total > 0:
                  return True



      def mark_paid(self):
            if self.check_done():
                  self.status="paid"
                  self.save()
            return self.status
#generate the order id 
def pre_save_cart_receiver(sender,instance,*args,**kwargs):
      if not instance.order_id:
            instance.order_id=unique_order_id_generator(instance)

      qs=Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
      if qs.exists():
            qs.update(active=False)
      
pre_save.connect(pre_save_cart_receiver,sender=Order)

#generate the order_total

#update order total when the product inside the cart changes
def post_save_cart_total(sender,instance,created,*args,**kwargs):
      if not created:
            cart_obj=instance
            cart_total=cart_obj.total 
            cart_id=cart_obj.id 
            qs=Order.objects.filter(cart__id=cart_id)
            if qs.exists() and qs.count()==1:
                  order_obj=qs.first()
                  order_obj.update_total()



post_save.connect(post_save_cart_total,sender=Cart)


#also update the total when the order is newly createdd
def post_save_order(sender,instance,created,*args,**kwargs):
      if created:
            instance.update_total()





post_save.connect(post_save_order,sender=Order)