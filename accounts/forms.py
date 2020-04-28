from django import forms 
from django.contrib.auth import get_user_model



class LoginForm(forms.Form):
      username=forms.CharField(max_length=120)
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



class GuestForm(forms.Form):
      email=forms.EmailField()