from django.shortcuts import render,redirect
from django.utils.http import is_safe_url

# Create your views here.
from .forms import AddressModelForm
from billing.models import BillingProfile
from .models import Address
def checkout_address_create_view(request):
      form=AddressModelForm(request.POST or None)
      next_ = request.GET.get('next')
      next_post = request.POST.get('next')
      redirect_path=next_ or next_post or None 

      if form.is_valid():
            instance=form.save(commit=False)
            billing_profile,billing_profile_created=BillingProfile.objects.new_or_get(request)
            if billing_profile is not None:
                  print(request.POST)
                  address_type=request.POST.get('address_type','shipping')
                  instance.billing_profile=billing_profile 
                  instance.address_type=address_type
                  address_type_id=address_type+'_address_id'
                  instance.save() 
                  request.session[address_type_id]=instance.id           

            if is_safe_url(redirect_path,request.get_host()):
                  return redirect(redirect_path)

            else:
                  return redirect('cart:cart-checkout')
      else:
            print('form is not valid')
      return redirect("cart:checkout") 




def checkout_address_reuse_view(request):

      next_ = request.GET.get('next')
      next_post = request.POST.get('next')
      redirect_path=next_ or next_post or None 

      if request.method=="POST":
            billing_profile,billing_profile_created=BillingProfile.objects.new_or_get(request)
            address_id=request.POST.get("address_id")
            if address_id :
                  address_qs=Address.objects.filter(id=address_id,billing_profile=billing_profile)
                  if address_qs.exists() and address_qs.count()==1:
                        address_obj=address_qs.first()
                        address_type=request.POST.get('address_type','shipping')
                        request.session[address_type+'_address_id']=address_obj.id 
                  else:
                        print("error geiing address")


            if is_safe_url(redirect_path,request.get_host()):
                  return redirect(redirect_path)

            else:
                  return redirect('cart:checkout')
      else:
            print('form is not valid')
      return redirect("cart:checkout") 