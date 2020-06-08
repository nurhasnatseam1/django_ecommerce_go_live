import os 
from django.db import models
import random
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.db.models import Q
from django.db.models.signals import post_save,pre_save
from .utils import random_stirng_generator,unique_slug_generator 
# Create your models here.
from ecommerce.utils import get_filename




def get_filename_ext(filename):
      base_name=os.path.basename(filename)
      print(base_name)
      name,ext=os.path.splitext(base_name)
      return name,ext

def uploadImagePath(instance, filename):

      print(filename)
      new_filename=random.randint(1,99999999)
      name,ext=get_filename_ext(filename)
      final_filename=f"products/{instance.id}/{new_filename}.{ext}"
      return final_filename

def uploadFilePath(instance, filename):

      print(filename)
      new_filename=random.randint(1,99999999)
      name,ext=get_filename_ext(filename)
      final_filename=f"products/{instance.id}/{new_filename}.{ext}"
      return final_filename

class ProductsCustomQuerySet(models.query.QuerySet):
      """meaning custom filtering of the queryset of the model"""
      def active(self):
            return self.filter(active=True)


      def featured(self):
            return self.filter(featured=True,active=True)

      def search(self,query):
            return self.filter(Q(title__icontains=query)|Q(description__icontains=query)|Q(tags__title__icontains=query)).distinct()



class ProductModelManager(models.Manager):

      def get_queryset(self):
            return ProductsCustomQuerySet(self.model,using=self._db)

      def get_by_id(self,id=1):
            qs= self.get_queryset().filter(id=id)
            if qs.exists() and qs.count()==1:
                  return qs.first()
            else:
                  return None

      def featured(self):
            return self.get_queryset().featured()
      
      def all(self):
            return self.get_queryset().active()#get_queryset() returns all products 

      def search(self,query):
            if query is not None:
                  qs=Product.objects.featured().search(query)
                  return qs
            return Product.objects.featured()

class Product(models.Model):
      title       = models.CharField(max_length=120)
      slug        = models.SlugField(blank=True,unique=True)
      description = models.TextField()
      price       = models.DecimalField(decimal_places=2,max_digits=10,default=39.99)
      image       = models.ImageField(upload_to=uploadImagePath,null=True,blank=True)
      featured    = models.BooleanField(default=False)
      active      = models.BooleanField(default=True)
      timestamp   = models.DateTimeField(auto_now_add=True)
      is_digital  = models.BooleanField(default=False)


      objects=ProductModelManager()
      def __str__(self):
            return self.title


      def get_absolute_url(self):
            return reverse("products:detail",kwargs={"slug":self.slug})

      def get_downlaods(self):
            qs=self.productfile_set.all()
            return qs

      def get_absolute_url(self):
            return reverse('products:detail',kwargs={'slug':self.slug})


def pre_save_receiver(sender,instance,*args,**kwargs):
      if not instance.slug:
            instance.slug=unique_slug_generator(instance)
      

pre_save.connect(pre_save_receiver,sender=Product)

def upload_product_file_loc(instance,filename):
      """it does not have instance.id"""
      slug=instance.product.slug 
      if slug:
            location=f"/product/{slug}/"
      else:
            slug=unique_slug_generator(instance.product)
            location = f"product/{slug}"
      return location + filename


class ProductFile(models.Model):
      product     = models.ForeignKey(Product,on_delete=models.CASCADE)
      file        = models.FileField(
            upload_to=upload_product_file_loc,
            storage=FileSystemStorage(location=settings.PROTECTED_ROOT)
            )# overrideing default storage settings of going to the  media root with this settings but this is not specifying to use a secure url the url wil still at /media/ endpoint because of static url settings in urls.py
      free       = models.BooleanField(default=False)
      user_required=models.BooleanField(default=False)



      def __str__(self):
            return str(self.file.name)


      def get_default_url(self):
            return self.product.get_absolute_url()


      def get_download_url(self):
            return reverse('orders:download',kwargs={"slug":self.product.slug,"pk":self.pk})

      @property 
      def name(self):
            return get_filename(self.file.name)