
from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import LoginForm,RegisterForm,GuestForm
from django.contrib.auth import authenticate,login,get_user_model
from django.utils.http import is_safe_url
# Create your views here.


from .models import GuestEmail

User=get_user_model()

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
                  email=form.cleaned_data.get("email")
                  password=form.cleaned_data.get("password")

                  user=authenticate(email=email,password=password)
                  print(user)
                  print(redirect_path)

                  if user is not None:
                        try:
                              del request.session["guest_email_id"]
                        except:
                              pass
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
                  email=form.cleaned_data.get("email")
                  password=form.cleaned_data.get("password")
                  email=form.cleaned_data.get("email")

                  user=authenticate(email=email,password=password)

                  if user is not None:
                        login(request,user)
                        return redirect('products:list')
                  else:
                        user=User.objects.create(email=email)
                        user.set_password(password)
                        user.save()
                        login(request,user)
                        return redirect('products:list')
      return render(request,"accounts/register.html",context)




def guest_login_view(request):
      form = GuestForm(request.POST or None)

      context={
            "form":form
      }
      next_ =request.GET.get('next')
      next_post=request.POST.get('next')
      redirect_path=next_ or next_post or None

      if form.is_valid():
            email=form.cleaned_data.get("email")
            new_guest_email=GuestEmail.objects.create(email=email)
            request.session["guest_email_id"] = new_guest_email.id
            if is_safe_url(redirect_path,request.get_host()):
                  return redirect(redirect_path)
            else:
                  return redirect("/")

      return redirect("register")
