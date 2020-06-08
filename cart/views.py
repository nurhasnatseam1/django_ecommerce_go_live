from django.shortcuts import render,redirect,HttpResponseRedirect
from django.conf import settings
# Create your views here.

from .models import Cart
from products.models import Product
from orders.models import Order 
from accounts.forms import LoginForm,GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
from address.forms import AddressModelForm
from address.models import Address
from django.http import JsonResponse



def cart_detail_api_view(request):
      cart_obj,new_obj =Cart.objects.new_or_get(request)
      products=[{'title':x.title,'price':x.price,'slug':x.slug,'id':x.id} for x in cart_obj.products.all()] #you can do this, or import rest framework and serialize the cart object
      return JsonResponse({'products':products,'subtotal':cart_obj.subtotal,'total':cart_obj.total})

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
            product_added=False
            cart_obj.products.remove(product_obj)
      else:
            cart_obj.products.add(product_obj)
            product_added=True
      if request.is_ajax():
            return JsonResponse({
                  "added":product_added,
                  "removed":not product_added,
            })
      return redirect("cart:cart-home")


STRIPE_PUB_KEY=settings.STRIPE_PUB_KEY
def checkout_home(request):
      cart_obj,cart_created=Cart.objects.new_or_get(request)
      if  cart_created or cart_obj.products.count()==0:
            return redirect("cart:cart-home")

      user=request.user 
      login_form=LoginForm()
      guest_form=GuestForm()
      address_form=AddressModelForm()
      billing_address_form=AddressModelForm()

      shipping_address_required=not cart_obj.is_digital


      billing_address_id=request.session.get('billing_address_id',None)
      shipping_address_id=request.session.get('shipping_address_id',None)

      print("shipping_address_id",shipping_address_id)
      print('billing_address_id',billing_address_id)
      print(request.session)

      has_card=False

      billing_profile,billing_profile_created=BillingProfile.objects.new_or_get(request)

      if billing_profile is not None:
            address_qs=Address.objects.filter(billing_profile=billing_profile)
            order_obj,order_obj_created=Order.objects.new_or_get(billing_profile,cart_obj)
            if shipping_address_id:
                  print(shipping_address_id)
                  order_obj.shipping_address=Address.objects.get(id=shipping_address_id)
                  del request.session["shipping_address_id"]
            if billing_address_id:
                  order_obj.billing_address=Address.objects.get(id=billing_address_id)
                  del request.session["billing_address_id"] 
            if billing_address_id or shipping_address_id:
                  order_obj.save()
            has_card=billing_profile.has_card
      else:
            order_obj=None
            address_qs=None

      

      if request.method == "POST":
            is_done = order_obj.check_done()
            if is_done:
                  charge_paid,charge_msg=billing_profile.charge(order_obj)
                  if charge_paid:
                        order_obj.mark_paid()
                        del request.session['cart_id']
                        if not billing_profile.user:
                              billing_profile.set_cards_inactive()
                              del request.session['guest_email_id']
                        return redirect('/order/success') 
                  else:
                        print('charge was not paid to stripe via card')  
      context={
            "object":order_obj,
            "cart":cart_obj,
            "address_form":address_form,
            "billing_address_form":billing_address_form,
            "billing_profile":billing_profile,
            "login_form":login_form,
            "guest_form":guest_form,
            "address_qs":address_qs,
            "has_card":has_card,
            "publish_key":STRIPE_PUB_KEY,
            "shipping_address_required":shipping_address_required,
            }
      return render(request,'cart/checkout.html',context)
