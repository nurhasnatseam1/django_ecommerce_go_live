
from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,get_user_model
from django.utils.http import is_safe_url
# Create your views here.


def login_page(request):
      context={}
      form=LoginForm(request.POST or None)
      context["form"]=form
      print(request.GET)
      next_=request.GET.get('next')
      next_post=request.POST.get('next')
      redirect_path=next_ or next_post or None
      print(request.POST)
      if request.method=="POST":
            if form.is_valid():
                  username=form.cleaned_data.get("username")
                  password=form.cleaned_data.get("password")

                  user=authenticate(username=username,password=password)
                  print(user)
                  print(redirect_path)

                  if user is not None:
                        login(request,user)
                        if is_safe_url(redirect_path,request.get_host()):
                              return HttpResponseRedirect(redirect_path)
                        return redirect("login")
      return render(request,"accounts/login.html",context)



def register_page(request):
      context={}
      form= RegisterForm(request.POST or None)
      context["form"]=form

      if request.method == "POST":
            if form.is_valid():
                  username=form.cleaned_data.get("username")
                  password=form.cleaned_data.get("password")
                  email=form.cleaned_data.get("email")

                  user=authenticate(username=username,password=password)

                  if user is not None:
                        login(request,user)
                        return redirect('login')
                  else:
                        user=User.objects.create(username=username,password=password,email=email)
                        login(request,user)
                        return redirect('login')
      return render(request,"accounts/register.html",context)