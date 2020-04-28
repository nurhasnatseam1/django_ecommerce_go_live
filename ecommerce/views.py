from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,get_user_model

User=get_user_model()
def base(request):
      print(request.user)
      return render(request,"home.html",{})




def login_page(request):
      context={}
      form=LoginForm(request.POST or None)
      context["form"]=form
      if request.method=="POST":
            if form.is_valid():
                  username=form.cleaned_data.get("username")
                  password=form.cleaned_data.get("password")

                  user=authenticate(username=username,password=password)

                  if user is not None:
                        login(request,user)
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




      