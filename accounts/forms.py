from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField 
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
            fields=('email','password','active','admin')

      def clean_password(self):
            return self.initail['password']



class LoginForm(forms.Form):
      email=forms.EmailField(max_length=120,label='Email')
      password=forms.CharField(max_length=30,widget=forms.PasswordInput)




class RegisterForm(forms.Form):
      username=forms.CharField()
      email=forms.EmailField()
      password=forms.CharField(widget=forms.PasswordInput)
      password_2=forms.CharField(label='confirm_password',widget=forms.PasswordInput)


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