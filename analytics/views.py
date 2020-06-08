from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import TemplateView 
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from orders.models import Order
from django.utils import timezone
import datetime



class SalesView(LoginRequiredMixin,TemplateView):
      template_name='analytics/sales.html'


      def dispatch(self,*args,**kwargs):
            user = self.request.user 
            if not user.is_staff:
                  return render(self.request,"400.html",{})
            return super().dispatch(*args,**kwargs)
      
      def get_context_data(self,*args,**kwargs):
            context = super().get_context_data(*args,**kwargs)
            context['this_week']=Order.objects.all().by_weeks_range(weeks_ago=1,number_of_weeks=10).get_sales_breakdown()
            context['last_four_weeks']=Order.objects.all().by_weeks_range(weeks_ago=10,number_of_weeks=7).get_sales_breakdown()
            context['today']=Order.objects.all().by_range(start_date=timezone.now().date()).get_sales_breakdown(     )
            return context
