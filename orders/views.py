from django.shortcuts import render

# Create your views here.
def order_sucess(request):
      return render(request,"orders/success.html",{})