from django.shortcuts import render,redirect,HttpResponseRedirect

# Create your views here.

from .models import Cart
from products.models import Product

def cart_home(request):

      """ cart_id=request.session.get("cart_id")

      qs=Cart.objects.filter(id=cart_id)
      if qs.count()==1:
            print("cart id exists")
            cart_obj=qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                  cart_obj.user =request.user
                  cart_obj.save()
      else:
            cart_obj=Cart.objects.new(user=None)
            request.session['cart_id']=cart_obj.id """

      cart_obj,new_obj=Cart.objects.new_or_get(request)
      context={
            "cart":cart_obj
      }
      return render(request,"cart/home.html",context)





def cart_update(request):
      print('POST:')
      print(request.POST)
      product_obj=Product.objects.get(id=request.POST.get("product"))
      cart_obj,new_obj=Cart.objects.new_or_get(request)
      if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
      else:
            cart_obj.products.add(product_obj)
      return redirect("cart:cart-home")