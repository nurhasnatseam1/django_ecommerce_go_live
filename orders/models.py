from django.db import models
from django.db.models.signals import pre_save,post_save
import math
from decimal import Decimal
from django.conf import settings 
# Create your models here.
from billing.models import BillingProfile
from cart.models import Cart
from ecommerce.utils import unique_order_id_generator
from address.models import Address
from products.models import Product
from datetime import datetime
from django.db.models import Sum,Avg,Count
ORDER_STATUS_CHOICES=(
      ('created','Created'),
      ('shipped','Shipped'),
      ('paid','Paid'),
      ('refunded',"Refunded"),
)


User=settings.AUTH_USER_MODEL

class OrderManagerQuerySet(models.query.QuerySet):

      def recent(self):
            return self.order_by("-updated","-timestamp")

      def by_request(self,request):
            billing_profile,created=BillingProfile.objects.new_or_get(request)
            return self.filter(billing_profile=billing_profile)

      def not_created(self):
            return self.exclude(status='created')

      def not_refunded(self):
            return self.exclude(status__iexact='refunded')

      def by_status(self,status='shipped'):
            return self.filter(status__iexact=status)
      
      def cart_data(self):
            return self.aggregate(
                  Sum('cart__products__price'),
                  Avg('cart__products__price'),
                  Count('cart_products'),
            )

      def totals_data(self):
            return self.aggregate(Sum('total'),Count('total'))

      def get_sales_breakdown(self):
            recent=self.recent().not_refunded()
            recent_data=recent.totals_data()
            recent_cart_data=recent.cart_data()
            shipped=recent.not_refunded().by_status(status='shipped')
            shipped_data=shipped.total_data()
            paid=recent.by_status(status='paid')
            data={
                  'recent':recentself.cart.products.all(),
                  'recent_data':recent_data,
                  'recent_cart_data':recent_cart_data,
                  'shipped':shipped,
                  'shipped_data':shipped_data,
                  'paid':paid,
            }
            return data
      def by_date(self): #sales from last these days
            target_date=timezone.now()-datetime.timedelta(days=1)#yesterday
            return self.filter(updated__day__gte=target_date.day)


      def by_range(self,start_ate,end_date=None):
            if end_date is None:
                  return self.filter(updated__gte=start_date)
            return self.filter(updated__gte=start_date).filter(updated__lte=end_date)
      
      def by_weeks_range(self,weeks_ago=7,number_of_weeks=2):
            if weeks_ago > number_of_weeks:
                  number_of_weeks=weeks_ago
            days_ago_start=weeks_ago *7 
            days_ago_end=weeks_ago -  (days_ago_start *7)
            start_date=timezone.now() - datetime.timedelta(days=days_ago_start)
            end_date=timezone.now() - datetime.timedelta(days=days_ago_end)

            return self.by_range(start_date=start_date,end_date=end_date)



class OrderManager(models.Manager):

      def get_queryset(self):
            return OrderManagerQuerySet(self.model,self._db)

      def by_request(self,request):
            return self.get_queryset().by_request(request)

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
            shipping_address_required=not self.cart.is_digital 
            shipping_done = False 

            if shipping_address_required and self.shipping_address:
                  shipping_done =True 
            elif shipping_address_required and not self.shipping_address:
                  shipping_done = False 
            else :
                  shipping_done = True 
            
            billing_profile=self.billing_profile
            shipping_address=self.shipping_address
            billing_address=self.billing_address 
            total=self.order_total 
            if total < 0:
                  return False 
            elif billing_profile and shipping_done and billing_address and total > 0:
                  return True

      def update_purchase(self):
            for p in self.cart.products.all():
                  obj,created=ProductPurchase.objects.get_or_create(
                        order_id=self.order_id,
                        product=p,
                        billing_profile=self.billing_profile
                  )
                  obj.refunded=False 
                  obj.save()
            return ProductPurchase.objects.filter(order_id=self.order_id).count()

      def mark_paid(self):
            if self.status != 'paid':
                  if self.check_done():
                        self.status="paid"
                        self.save()
                        self.update_purchase()
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



class ProductPurchaseQuerySet(models.query.QuerySet):
      def active(self):
            return self.filter(refunded=False)
      def digital(self):
            return self.filter(product__is_digital=True)



      def by_request(self,request):
            billing_profile,created=BillingProfile.objects.new_or_get(request)
            return self.filter(billing_profile=billing_profile)
class ProductPurchaseManager(models.Manager):

      def get_queryset(self):
            return ProductPurchaseQuerySet(self.model,using=self._db)

      def all(self):
              return self.get_queryset().active()

      def by_request(self,request):
            """returns all productPurchase of a particular billing profile"""
            return self.get_queryset().by_request(request)

      def digital(self):
            return self.get_queryset().active().digital()

      def products_by_request(self,request):
            """returning all the unique digital  products owned by a single billing_profile , you get the billing profile by the request  """
            qs=self.by_request(request).digital()
            ids_ = [x.product.id for x in qs]
            product_qs = Product.objects.filter(id__in = ids_).distinct()
            return product_qs

      def products_by_id(self,request):
            """returning all the unique digital  products owned by a single billing_profile , you get the billing profile by the request  """
            qs=self.by_request(request).digital()
            ids_ = [x.product.id for x in qs]
            return ids_




class ProductPurchase(models.Model):
      order_id          = models.CharField(max_length=120)
      billing_profile   = models.ForeignKey(BillingProfile,on_delete=models.DO_NOTHING)
      product           = models.ForeignKey(Product,on_delete=models.DO_NOTHING)  #even though product is a foreign key the one productPurchase instance can only have one product instance associated with it
      refunded          = models.BooleanField(default=False)
      timestamp         = models.DateTimeField(auto_now_add=True)
      updated           = models.DateTimeField(auto_now=True)
      
      
      
      objects=ProductPurchaseManager()
      def __str__(self):
            return self.product.title 