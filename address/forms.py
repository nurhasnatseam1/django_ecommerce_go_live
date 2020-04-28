from django import forms 




from .models import Address 




class AddressModelForm(forms.ModelForm):

      class Meta:
            model=Address 
            exclude=["billing_profile","address_type"]