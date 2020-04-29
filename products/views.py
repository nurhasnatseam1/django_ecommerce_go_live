from django.shortcuts import render,Http404
from django.views.generic import (ListView,
                                    DetailView)
# Create your views here.


from .models import Product 
from cart.models import Cart 
from analytics.signals import object_viewed_signal
from analytics.mixins import ObjectViewedMixin

class ProductListView(ListView):
      queryset          = Product.objects.all()
      template_name     = "products/product_list.html"



class ProductDetailView(ObjectViewedMixin,DetailView):
      queryset=Product.objects.all()
      template_name="products/product_detail.html"
      

      def get_context_data(self,*args,**kwargs):
            context=super().get_context_data(*args,**kwargs)
            cart_obj,new_obj=Cart.objects.new_or_get(self.request)
            context['cart']=cart_obj 
            return context

      def get_object(self,*args,**kwargs):
            obj = Product.objects.filter(slug=self.kwargs.get('slug')).first()
            if obj:
                  return obj 
            else:
                  Http404("object did not found")
                  return None 




class ProductFeaturedListView(ListView):
      template_name="products/product_list.html"


      def get_queryset(self,*args,**kwargs):
            qs=Product.objects.featured()
            return qs 



class ProductFeaturedDetailView(ObjectViewedMixin,DetailView):
      template_name="products/product_detail.html"

      def get_queryset(self,*args,**kwargs):
            qs=Product.objects.featured()
            return qs 



