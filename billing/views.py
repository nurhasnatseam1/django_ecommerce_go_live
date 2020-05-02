import stripe
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.utils.http import is_safe_url
from django.conf import settings
# Create your views here.

from billing.models import BillingProfile,Card

STRIPE_PUB_KEY=settings.STRIPE_PUB_KEY
def payment_method_view(request):
    billing_profile,billing_profile_created=BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect('/cart')
    next_url=None
    next_=request.GET.get('next')
    if is_safe_url(next_,request.get_host()):
         next_url=next_
    return render(request,'billing/payment-method.html',{"publish_key":STRIPE_PUB_KEY,"next_url":next_url})


#associate stripe customer id with billing profile
def payment_method_create_view(request):
    if request.method=="POST" and request.is_ajax():
        billing_profile,billing_profile_created=BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return JsonResponse({"message":"Cannot find this user"},status_code=401)
        token=request.POST.get('token')
        new_card_obj=Card.objects.add_new(billing_profile=billing_profile,token=token)
        print(new_card_obj)
        print('this is card information for you')


        return JsonResponse({"message":"Done"})
    return HttpResponse("error",status_code=401)
