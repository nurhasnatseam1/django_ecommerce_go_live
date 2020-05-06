
from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import OldLoginForm,ImprovedLoginForm,RegisterForm,GuestForm
from django.contrib.auth import authenticate,login,get_user_model
from django.utils.http import is_safe_url
from django.views.generic import DetailView,FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import View,FormView,CreateView
from django.urls import reverse 
from django.utils.safestring import mark_safe



from .models import EmailActivationForLogin
from .forms import ReactivateEmailForm
from ecommerce.mixins import NextUrlMixin
# Create your views here.
#difference between form view and create and update view is (create and update view has form_valid method built in on them )
#use create and update view when working with a model or when you do not need power over how the form is validating

#else any view should use formview if it needs form in context and a post message

from .models import GuestEmail

User=get_user_model()

@login_required
def account_home_view(request):
      return render(request,'accounts/home.html',{})



class AccountHomeView(LoginRequiredMixin,DetailView):
      template_name='accounts/home.html'

      def get_object(self,*args,**kwargs):
            return self.request.user 







def login_page(request):
      context={}
      form=OldLoginForm(request.POST or None)
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






class ImprovedLoginView(NextUrlMixin,FormView):
      form_class=ImprovedLoginForm 
      success_url='/'
      template_name='accounts/login.html'


      #this is equavalent to form=formClass(arguments:request.POST)
      def get_form_kwargs(self):
            kwargs=super().get_form_kwargs()
            kwargs['request']=self.request
            return kwargs


      def form_valid(self,form):
            request=self.request 
            user=form.user 
            if user is not None:
                  if not user.is_active:
                        return super().form_invalid(form)
                  if user.is_authenticated:
                        next_path=self.get_next_url()
                        return redirect(next_path)
            return super().form_invalid(form)






class OldLoginView(FormView):
      form_class=OldLoginForm 
      success_url='/'
      template_name='accounts/login.html'


      #this is equavalent to form=formClass(arguments:request.POST)
      def get_form_kwargs(self):
            kwargs=super().get_form_kwargs()
            kwargs['request']=self.request
            return kwargs


      def form_valid(self,form):
            request=self.request 
            next_=request.GET.get('next')
            next_post=request.POST.get('next')
            redirect_path=next_ or next_post or None 

            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')

            user=authenticate(request,username=email,password=password)

            if user is not None:
                  if not user.is_active():
                        messages.error(request,'This user is inactive')
                        return super().form_invalid(form)
                  login(request,user)
            #      user_logge_in.send(user.__class__,instance=user,request=request)
                  try:
                        del request.session['guest_email_id']
                  except:
                        pass 
                  if is_safe_url(redirect_path,request.get_host()):
                        return redirect(redirect_path)
                  else:
                        return redirect('/')
                  
            return super().form_invalid(form)




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



class RegisterView(CreateView):
      form_class=RegisterForm
      template_name='accounts/register.html'
      success_url='/account/login.html'      




class ActivateAccountView(View):
      key=None
      def get(self,request,key=None,*args,**kwargs):
            self.key=key
            if key is not None:
                  qs=EmailActivationForLogin.objects.confirmable().filter(key__iexact=key)
                  confirm_qs=qs.confirmable()
                  if confrim_qs.count()==1:
                        obj=confirm_qs.first()
                        obj.activate()
                        messages.success(request,"you have activated your account,enjoy our site")
                        return redirect('login')
                  else:
                        activated_qs=qs.filter(activated=True) 
                        if activated.exists():
                              reset_link=reverse("password_reset")
                              msg=f"""
                              your email has already been confirmed,
                              do you want to change your password
                              then go there <a href='{reset_link}' >change password</a>
                              """
                              messages.success(request,mark_safe(msg))
                              return redirect("login")
            
            context={
                  "form":ReactivateEmailForm(),
                  "key":key
            }
            return render(request,'registration/activtion-error.html',context)

      def post(self,request,*args,**kwargs):
            form = ReactivateEmailForm(request.POST or None)
            if form.is_vaild():
                  email=form.cleaned_data.get('email')
                  qs=EmailActivationForLogin.objects.email_exists(email=email)
                  obj=qs.first()
                  user=obj.user 
                  obj.regenerate()
                  obj.send_activation()
                  messages.success(request,mark_safe('your activation link has sent to your email'))
            else:
                  messages.error(request,"there was a problem parsing your email address")
            context={
                  "form":form,
            }
            #if there is and error in the form the form validation will be shown by the help of the form object itself
            return render(request,'registration/activation-error.html',context)
