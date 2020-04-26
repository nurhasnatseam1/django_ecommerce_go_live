from django.shortcuts import render
from django.views import generic
from django.db.models import Q
# Create your views here.

from products.models import Product 



class ProductSearchView(generic.ListView):
      template_name='search/search_view.html'


      def get_queryset(self,*args,**kwargs):
            request=self.request 
            query=self.request.GET.get("q")
            return Product.objects.search(query)