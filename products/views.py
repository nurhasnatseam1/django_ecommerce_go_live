from django.shortcuts import render,Http404
from django.views.generic import (ListView,
                                    DetailView)
# Create your views here.


from .models import Product 




class ProductListView(ListView):
      queryset          = Product.objects.all()
      template_name     = "products/product_list.html"



class ProductDetailView(DetailView):
      queryset=Product.objects.all()
      template_name="products/product_detail.html"
      

      def get_object(self,*args,**kwargs):
            obj = Product.objects.get(slug=self.kwargs.get('slug'))
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



class ProductFeaturedDetailView(DetailView):
      template_name="products/product_detail.html"

      def get_queryset(self,*args,**kwargs):
            qs=Product.objects.featured()
            return qs 



