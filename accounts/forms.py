from django import forms 
from django.contrib.auth import get_user_model,authenticate,login
from django.contrib.auth.forms import ReadOnlyPasswordHashField 
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.urls import reverse 

User=get_user_model()

class UserAdminCreationForm(forms.ModelForm):
      password1=forms.CharField(label="password",widget=forms.PasswordInput)
      password2=forms.CharField(label='confirm password',widget=forms.PasswordInput)


      class Meta:
            model=User 
            fields=('email','password1','password2')


      def clean_password2(self):
            password1=self.cleaned_data.get("password1")
            password2=self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                  raise forms.ValidationError("password's do not match")
            return password2


      def save(self,commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data.get("password2"))
            if commit :
                  user.save()
            return user


class UserAdminChangeForm(forms.ModelForm):
      password=ReadOnlyPasswordHashField()

       


      class Meta:
            model=User
            fields=('email','password','is_active','admin')

      def clean_password(self):
            return self.initail['password']



class ImprovedLoginForm(forms.Form):
      email=forms.EmailField(max_length=120,label='Email')
      password=forms.CharField(max_length=30,widget=forms.PasswordInput)

      def __init__(self,request,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.request=request 

      def clean(self):
            request=self.request 
            data=self.cleaned_data
            email=data.get('email')
            password=data.get('password')
            user = authenticate(request,email=email,password=password)
            qs=User.objects.filter(email=email)
            if qs.exists():
                  not_active=qs.filter(is_active=False)
                  if not_active.exists():
                        resend_link=reverse('accounts:resend_activate_email')
                        reconfirm_msg="""
                        <a href='{resend_link}' >resend confirmation email to this email </a>
                        """
                        confirm_email=EmailActivation.objects.filter(email=email)
                        is_confirmable=confirm_email.confirmable().exists()
                        if is_confirmable:
                              raise forms.ValidationError("Please check your email to confirm your account, we sent you an email activation link",reconfirm_msg)
                        email_exists_but_not_confirmable_qs=EmailActivation.objects.email_exists(email)
                        email_exists_but_not_confirmable_exists=email_exists_but_not_confirmable_qs.exits()
                        if email_exists_but_not_confirmable_exists:
                              raise forms.ValidationError(mark_safe(reconfirm_msg))
                        if not is_confirmable and not email_exists_but_not_confirmable_exists:
                              raise forms.ValidationError("This user is inactive",reconfirm_msg)
            if user is None :
                  raise forms.ValidationError("Invalid credentials")
            if not user.is_active:
                  messages.error(request,'This user is inactive')
                  self.user=user
                  raise forms.ValidationError("This user is not activated by email activation")
            login(request,user)
            self.user=user 
            #      user_logge_in.send(user.__class__,instance=user,request=request)
            try:
                  del request.session['guest_email_id']
            except:
                  pass 
            return data




class OldLoginForm(forms.Form):
      emial=forms.EmailField(label='email')
      password=forms.CharField(widget=forms.PasswordInput)




class LoginForm(forms.Form):
      emial=forms.EmailField(label='email')
      password=forms.CharField(widget=forms.PasswordInput)









class RegisterForm(forms.ModelForm):


      email=forms.EmailField()
      password=forms.CharField(widget=forms.PasswordInput)
      password_2=forms.CharField(label='confirm_password',widget=forms.PasswordInput)


      class Meta:
            model=User 
            fields=['email','password','password_2']

      def clean_username(self):
            username=self.cleaned_data.get("username")
            qs=User.objects.filter(username=username)

            if qs.exists():
                  raise forms.ValidationError("Username already exists")
            return self.cleaned_data.get("username")

      def clean_password_2(self):
            password_value=self.cleaned_data.get("password")
            password_2_value=self.cleaned_data.get("password_2")
            if password_2_value != password_value:
                  raise forms.ValidationError("password and password_2 fields values do not match")
            return password_2_value


      def save(self,commit=True):
            user=super().save(commit=False)
            user.set_password(self.cleaned_data.get('password'))
            user.is_active=False 
            if commit:
                  user.save()
            return user



class GuestForm(forms.Form):
      email=forms.EmailField()




class ReactivateEmailForm(forms.Form):
      email=forms.EmailField()

      def clean_email(self):
            email=self.cleaned_data.get('email')
            qs=EmailActivation.objects.email_exists(email=email)
            if not  qs.exists():
                  link=reverse('accounts:register')
                  register_link=f"""
                        This email does not exists, would you like to <a href="{link}">register</a>
                  """
                  raise forms.ValidationError(mark_safe(register_link))
            return email